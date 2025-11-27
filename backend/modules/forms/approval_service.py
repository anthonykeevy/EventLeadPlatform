"""
Form Approval Service
Handles approval workflows for high-cost forms (Story 2.11)
Enhanced for External Approvers (Story 2.12)
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from decimal import Decimal
import secrets
import string

from models.form import Form
from models.ref.form_approval_status import FormApprovalStatus
from models.ref.form_status import FormStatus
from models.user import User
from models.form_approval_token import FormApprovalToken
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.audit.activity_log import ActivityLog
from common.config_service import ConfigurationService
from common.email import email_service
from common.logger import get_logger
from common.email_templates import get_approval_email_template, get_decision_email_template
from modules.users.external_user_service import ExternalUserService
from .access_guard import check_form_access_guard
import os

logger = get_logger(__name__)

class ApprovalService:
    
    def __init__(self, db: Session):
        self.db = db
        self.config_service = ConfigurationService(db)
        self.external_user_service = ExternalUserService(db)

    async def _get_status_by_code(self, code: str) -> Optional[FormApprovalStatus]:
        return self.db.execute(
            select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == code)
        ).scalar_one_or_none()

    async def _get_form_status_by_code(self, code: str) -> Optional[FormStatus]:
        return self.db.execute(
            select(FormStatus).where(FormStatus.StatusCode == code)
        ).scalar_one_or_none()

    async def submit_for_approval(self, form_id: int, user_id: int, company_id: int) -> Form:
        """
        Submit a form for approval (Internal).
        Transitions status to PENDING.
        """
        # Check access (Manage)
        form = await check_form_access_guard(self.db, form_id, user_id, "MANAGE")
        
        # Verify cost threshold
        threshold = self.config_service.get_approval_cost_threshold()
        cost = form.DeploymentCost or 0
        
        if cost <= threshold:
            logger.info(f"Form {form_id} cost {cost} is below threshold {threshold}. Proceeding anyway.")
            pass 
            
        # Get PENDING status
        pending_status = await self._get_status_by_code('PENDING')
        if not pending_status:
            raise ValueError("Approval Status 'PENDING' not found in database.")
            
        # Update status
        old_status_id = form.FormApprovalStatusID
        form.FormApprovalStatusID = pending_status.FormApprovalStatusID
        form.UpdatedBy = user_id
        form.UpdatedDate = datetime.utcnow()
        
        self.db.flush()
        
        # Log
        self._log_activity(user_id, company_id, "form.submitted_for_approval", form, 
                           f"Status: {old_status_id} -> {pending_status.FormApprovalStatusID}")
                           
        # Send Notifications to Admins
        await self._notify_admins_of_request(form, user_id, company_id)
        
        return form

    async def request_external_approval(self, form_id: int, requestor_id: int, company_id: int, external_email: str) -> Dict[str, Any]:
        """
        Request approval from an external stakeholder.
        Creates a Shadow User if needed, generates a token, and notifies them.
        """
        # 1. Check Access
        form = await check_form_access_guard(self.db, form_id, requestor_id, "MANAGE")
        requestor = self.db.get(User, requestor_id)

        # 2. Fraud Prevention
        # A. Self-Approval Prevention
        if requestor.Email.lower() == external_email.lower():
            raise ValueError("Self-approval is not allowed. Please choose a different approver.")
            
        # B. Internal Domain Check (Configurable)
        allow_internal_val = self.config_service.get_setting('forms.approval.allow_internal_domains', False)
        # Handle both boolean (from typed config) and string (from raw DB/default) cases
        allow_internal = str(allow_internal_val).lower() in ('true', '1', 'yes') if isinstance(allow_internal_val, str) else bool(allow_internal_val)
        
        if not allow_internal:
            requestor_domain = requestor.Email.split('@')[1]
            external_domain = external_email.split('@')[1]
            if requestor_domain.lower() == external_domain.lower():
                # Check if it's really an external user (maybe a colleague)
                # If it's a colleague, they should probably use the internal flow, but let's see.
                # The story implies preventing "Internal Domain Usage" to force internal workflow.
                # But we might want to allow it if they are not in the system? 
                # Sticking to strict interpretation: Block if domain matches.
                raise ValueError(f"Approval requests to internal domain ({requestor_domain}) are restricted. Use internal approval flow.")

        # C. Internal User Permission Check
        # Check if the target email belongs to an existing user in this company
        # If so, ensure they have 'company_admin' privileges.
        existing_member_role = self.db.execute(
            select(UserCompanyRole.RoleCode)
            .join(UserCompany, UserCompany.UserCompanyRoleID == UserCompanyRole.UserCompanyRoleID)
            .join(User, User.UserID == UserCompany.UserID)
            .where(
                User.Email == external_email,
                UserCompany.CompanyID == company_id,
                UserCompany.IsDeleted == False
            )
        ).scalar_one_or_none()

        if existing_member_role:
            # User is a member of this company
            if existing_member_role != 'company_admin':
                raise ValueError(f"User {external_email} is a member of this company but does not have approval permissions.")

        # 3. Get/Create Shadow User
        external_user, created_new = await self.external_user_service.get_or_create_external_user(external_email)
        
        # 4. Set Status to PENDING
        pending_status = await self._get_status_by_code('PENDING')
        form.FormApprovalStatusID = pending_status.FormApprovalStatusID
        form.UpdatedBy = requestor_id
        form.UpdatedDate = datetime.utcnow()
        
        # 5. Generate Token
        token_str = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7) # 7 day expiry
        
        token = FormApprovalToken(
            FormID=form_id,
            Token=token_str,
            Email=external_email,
            UserID=external_user.UserID,
            ExpiresAt=expires_at,
            CreatedBy=requestor_id
        )
        self.db.add(token)
        self.db.flush()
        
        # 6. Notify External Approver
        await self._notify_external_approver(form, requestor, external_email, token_str)
        
        # 7. Log Activity
        self._log_activity(requestor_id, company_id, "form.external_approval_requested", form, 
                           f"Requested from {external_email}")

        # 8. Notify Admins (Transparency)
        await self._notify_admins_of_external_request(form, requestor, company_id, external_email)

        return {"message": "External approval requested", "token": token_str, "email": external_email}

    async def validate_approval_token(self, token_str: str) -> FormApprovalToken:
        """
        Validate a token string and return the token object.
        """
        token = self.db.execute(
            select(FormApprovalToken).where(FormApprovalToken.Token == token_str)
        ).scalar_one_or_none()
        
        if not token:
            raise ValueError("Invalid approval token.")
            
        if token.IsUsed:
            raise ValueError("This approval link has already been used.")
            
        if token.ExpiresAt < datetime.utcnow():
            raise ValueError("This approval link has expired.")
            
        return token

    async def decide_via_token(self, token_str: str, decision: str, reason: str = None) -> Form:
        """
        Execute an approval decision via a public token.
        Acting as the External User (Shadow User).
        """
        # 1. Validate Token
        token = await self.validate_approval_token(token_str)
        
        # 2. Get Context
        form = self.db.get(Form, token.FormID)
        user_id = token.UserID # The Shadow User
        
        # 3. Execute Decision
        # Check if form is still PENDING
        current_status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if current_status.ApprovalStatusCode != 'PENDING':
             raise ValueError(f"Form is no longer PENDING (Current: {current_status.ApprovalStatusCode})")

        if decision.upper() == 'APPROVE':
            # Logic similar to approve_form but bypassing Admin Role check for External User
            # But we still need to ensure the flow is valid.
            
            approved_status = await self._get_status_by_code('APPROVED')
            form.FormApprovalStatusID = approved_status.FormApprovalStatusID
            form.UpdatedBy = user_id # Shadow User
            form.UpdatedDate = datetime.utcnow()
            
            # Auto-Publish if it was pending
            # Note: We just updated the status to APPROVED in memory, so checking the *current* DB state 
            # using the same session might reflect that depending on autoflush. 
            # But wait, we just set form.FormApprovalStatusID. 
            # So let's check the INTENT. This flow is specifically for pending requests.
            # If the user got a token, the form WAS pending. We can safely assume we should try to publish.
            
            published_status = await self._get_form_status_by_code('PUBLISHED')
            if published_status:
                form.FormStatusID = published_status.FormStatusID
                logger.info(f"Auto-publishing form {form.FormID} after external approval")
                
            self._log_activity(user_id, form.CompanyID, "form.approved_external", form, 
                               f"Approved by external user {token.Email}")
            
            # Notify Owner
            await self._notify_owner_of_decision(form, "Approved", user_id)
            
        elif decision.upper() == 'REJECT':
            if not reason:
                raise ValueError("Reason is required for rejection.")
                
            rejected_status = await self._get_status_by_code('REJECTED')
            form.FormApprovalStatusID = rejected_status.FormApprovalStatusID
            form.UpdatedBy = user_id
            form.UpdatedDate = datetime.utcnow()
            
            self._log_activity(user_id, form.CompanyID, "form.rejected_external", form, 
                               f"Rejected by external user {token.Email}. Reason: {reason}")
                               
            # Notify Owner
            await self._notify_owner_of_decision(form, "Rejected", user_id, reason)
            
        else:
            raise ValueError(f"Invalid decision: {decision}")
            
        # 4. Mark Token as Used
        token.IsUsed = True
        token.UsedAt = datetime.utcnow()
        
        self.db.flush()
        return form

    async def approve_form(self, form_id: int, admin_user_id: int, company_id: int) -> Form:
        """
        Approve a pending form (Internal Admin).
        Transitions status to APPROVED.
        """
        # 1. Check MANAGE access (base requirement)
        form = await check_form_access_guard(self.db, form_id, admin_user_id, "MANAGE")
        
        # 2. Check Company Admin Role (Strict enforcement per AC-2.11.3)
        # Owners have MANAGE but shouldn't self-approve if not admin
        await self._check_company_admin_role(admin_user_id, company_id)
        
        # Verify current status is PENDING or NO_APPROVAL (Pre-approval)
        current_status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if current_status.ApprovalStatusCode not in ['PENDING', 'NO_APPROVAL']:
             raise ValueError(f"Form is not in PENDING or DRAFT state (Current: {current_status.ApprovalStatusCode})")
             
        # Get APPROVED status
        approved_status = await self._get_status_by_code('APPROVED')
        if not approved_status:
            raise ValueError("Approval Status 'APPROVED' not found.")
            
        # Update Approval Status
        old_approval_status_code = current_status.ApprovalStatusCode
        form.FormApprovalStatusID = approved_status.FormApprovalStatusID
        form.UpdatedBy = admin_user_id
        form.UpdatedDate = datetime.utcnow()
        
        # Auto-Publish Logic
        # If form was PENDING (intercepted publish), auto-publish it.
        if old_approval_status_code == 'PENDING':
            published_status = await self._get_form_status_by_code('PUBLISHED')
            if published_status:
                form.FormStatusID = published_status.FormStatusID
                logger.info(f"Auto-publishing form {form_id} after approval")
        
        self.db.flush()
        
        # Log
        self._log_activity(admin_user_id, company_id, "form.approved", form, 
                           f"Approved by user {admin_user_id}")

        # Notify Owner
        if admin_user_id != form.CreatedBy:
            await self._notify_owner_of_decision(form, "Approved", admin_user_id)
        else:
            logger.info(f"Skipping owner notification for form {form_id} as approver {admin_user_id} is the owner.")
        
        return form

    async def reject_form(self, form_id: int, admin_user_id: int, company_id: int, reason: str) -> Form:
        """
        Reject a pending form.
        Transitions status to REJECTED.
        """
        # 1. Check MANAGE access
        form = await check_form_access_guard(self.db, form_id, admin_user_id, "MANAGE")
        
        # 2. Check Company Admin Role
        await self._check_company_admin_role(admin_user_id, company_id)
        
        current_status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        # Allow rejecting from PENDING or APPROVED? Usually from PENDING.
        
        rejected_status = await self._get_status_by_code('REJECTED')
        if not rejected_status:
            raise ValueError("Approval Status 'REJECTED' not found.")
            
        old_status_id = form.FormApprovalStatusID
        form.FormApprovalStatusID = rejected_status.FormApprovalStatusID
        form.UpdatedBy = admin_user_id
        form.UpdatedDate = datetime.utcnow()
        
        self.db.flush()
        
        self._log_activity(admin_user_id, company_id, "form.rejected", form, 
                           f"Reason: {reason}")
                           
        await self._notify_owner_of_decision(form, "Rejected", admin_user_id, reason)
        
        return form

    def check_publish_guard(self, form: Form) -> bool:
        """
        Check if form can be published.
        Returns True if allowed, raises ValueError if blocked.
        """
        threshold = self.config_service.get_approval_cost_threshold()
        cost = form.DeploymentCost or 0
        
        if cost <= threshold:
            return True
            
        # High cost - check approval
        status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if status.ApprovalStatusCode == 'APPROVED':
            return True
            
        raise ValueError(f"Form requires approval (Cost ${cost} > ${threshold}) and current status is {status.ApprovalStatusCode}")

    def _log_activity(self, user_id: int, company_id: int, action: str, form: Form, details: str):
        try:
            activity_log = ActivityLog(
                UserID=user_id,
                CompanyID=company_id,
                Action=action,
                EntityType="Form",
                EntityID=form.FormID,
                NewValue=details,
                CreatedDate=datetime.utcnow()
            )
            self.db.add(activity_log)
        except Exception as e:
            logger.warning(f"Failed to log activity: {e}")

    async def _check_company_admin_role(self, user_id: int, company_id: int):
        """Check if user is a Company Admin (or System Admin)"""
        # Check Company Role
        result = self.db.execute(
            select(UserCompany)
            .join(UserCompanyRole)
            .where(
                UserCompany.UserID == user_id,
                UserCompany.CompanyID == company_id,
                UserCompanyRole.RoleCode == 'company_admin',
                UserCompany.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if result:
            return True
            
        # Check System Admin
        user = self.db.get(User, user_id)
        if user:
            # Load role relationship if needed, or query
            from models.ref.user_role import UserRole
            role = self.db.execute(
                select(UserRole).where(UserRole.UserRoleID == user.UserRoleID)
            ).scalar_one_or_none()
            
            if role and role.RoleCode == 'system_admin':
                return True
        
        raise ValueError("Only Company Administrators can perform this action.")

    async def _notify_admins_of_request(self, form: Form, requestor_id: int, company_id: int):
        """
        Send email to all company admins.
        """
        # Find admins
        admins = self.db.execute(
            select(User)
            .join(UserCompany, User.UserID == UserCompany.UserID)
            .join(UserCompanyRole, UserCompany.UserCompanyRoleID == UserCompanyRole.UserCompanyRoleID)
            .where(
                UserCompany.CompanyID == company_id,
                UserCompanyRole.RoleCode == 'company_admin', # Corrected role code
                User.IsDeleted == False
            )
        ).scalars().all()
        
        if not admins:
            logger.warning(f"No admins found for company {company_id} to notify.")
            return

        requestor = self.db.get(User, requestor_id)
        requestor_name = f"{requestor.FirstName} {requestor.LastName}" if requestor else "Unknown User"

        subject = f"Approval Request: {form.FormName}"
        
        # Frontend URL for deep linking
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        view_url = f"{frontend_url}/dashboard?formId={form.FormID}"
        
        # Generate HTML content
        body = get_approval_email_template(
            form_name=form.FormName,
            requestor_name=requestor_name,
            cost=form.DeploymentCost,
            view_url=view_url
        )
        
        for admin in admins:
            try:
                await email_service.send_notification_email(admin.Email, subject, body)
            except Exception as e:
                logger.error(f"Failed to send approval email to admin {admin.Email}: {e}")
            
        logger.info(f"Notified {len(admins)} admins about form {form.FormID}")

    async def _notify_owner_of_decision(self, form: Form, decision: str, decider_id: int, reason: str = None):
        owner = self.db.get(User, form.CreatedBy)
        if not owner:
            return
            
        subject = f"Form Approval Update: {form.FormName}"
        
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        view_url = f"{frontend_url}/dashboard?formId={form.FormID}"
        
        body = get_decision_email_template(
            form_name=form.FormName,
            decision=decision,
            reason=reason,
            view_url=view_url
        )
        
        await email_service.send_notification_email(owner.Email, subject, body)
        logger.info(f"Notified owner {owner.Email} of decision: {decision}")

    async def _notify_external_approver(self, form: Form, requestor: User, email: str, token: str):
        """
        Send approval request to external user.
        """
        subject = f"Action Required: Please Approve '{form.FormName}'"
        
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        # Public approval URL
        approval_url = f"{frontend_url}/approval/external/{token}"
        
        # TODO: Create a dedicated template for external users?
        # For now, using a simple constructed body or we could add a new template.
        # Let's construct a simple HTML body here to keep it self-contained for this task.
        
        body = f"""
        <h2>Approval Request</h2>
        <p>Hello,</p>
        <p>{requestor.FirstName} {requestor.LastName} has requested your approval for the following form:</p>
        <p><strong>Form Name:</strong> {form.FormName}</p>
        <p><strong>Cost:</strong> ${form.DeploymentCost}</p>
        <br/>
        <p>Please review and approve or reject this request by clicking the link below:</p>
        <p><a href="{approval_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Review Request</a></p>
        <p>Or copy this link: {approval_url}</p>
        <p><small>This link is valid for 7 days.</small></p>
        """
        
        await email_service.send_notification_email(email, subject, body)
        logger.info(f"Sent external approval request to {email}")

    async def _notify_admins_of_external_request(self, form: Form, requestor: User, company_id: int, external_email: str):
        """
        Notify admins that an external approval has been requested (Transparency).
        """
        # Similar to _notify_admins_of_request but with different message
        admins = self.db.execute(
            select(User)
            .join(UserCompany, User.UserID == UserCompany.UserID)
            .join(UserCompanyRole, UserCompany.UserCompanyRoleID == UserCompanyRole.UserCompanyRoleID)
            .where(
                UserCompany.CompanyID == company_id,
                UserCompanyRole.RoleCode == 'company_admin',
                User.IsDeleted == False
            )
        ).scalars().all()
        
        if not admins:
            return

        subject = f"External Approval Requested: {form.FormName}"
        
        body = f"""
        <h2>External Approval Log</h2>
        <p>For your information, an external approval has been requested.</p>
        <ul>
            <li><strong>Requestor:</strong> {requestor.FirstName} {requestor.LastName}</li>
            <li><strong>External Approver:</strong> {external_email}</li>
            <li><strong>Form:</strong> {form.FormName}</li>
        </ul>
        <p>No action is required from you at this time.</p>
        """
        
        for admin in admins:
            try:
                await email_service.send_notification_email(admin.Email, subject, body)
            except Exception:
                pass 
