"""
Compliance Service
Generates comprehensive audit reports for Forms and Events (Story 2.13)
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, or_
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import json

from models.form import Form
from models.form_access_control import FormAccessControl
from models.form_approval_token import FormApprovalToken
from models.event import Event
from models.user import User
from models.company import Company
from models.audit.activity_log import ActivityLog
from models.ref.form_status import FormStatus
from models.ref.form_approval_status import FormApprovalStatus
from models.ref.form_access_control_access_type import FormAccessControlAccessType
from common.logger import get_logger

logger = get_logger(__name__)


def to_utc_iso(dt) -> Optional[str]:
    """Convert datetime to UTC ISO format with Z suffix for proper frontend parsing."""
    if dt is None:
        return None
    # Append 'Z' to indicate UTC - JavaScript Date() needs this to parse as UTC
    return dt.isoformat() + 'Z'


@dataclass
class AuditEntry:
    """Single audit trail entry"""
    timestamp: str
    action: str
    action_display: str
    user_id: Optional[int]
    user_email: Optional[str]
    user_name: Optional[str]
    is_external: bool
    details: Optional[str]
    old_value: Optional[str] = None  # For tracking changes (was)
    new_value: Optional[str] = None  # For tracking changes (now)
    token_id: Optional[int] = None
    # Additional context fields for Activity Log table
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    form_name: Optional[str] = None
    event_name: Optional[str] = None


@dataclass
class ApprovalChainEntry:
    """Approval chain entry"""
    approver_id: Optional[int]
    approver_email: str
    approver_name: Optional[str]
    is_external: bool
    decision: str
    decided_at: Optional[str]
    token_id: Optional[int]
    reason: Optional[str]


@dataclass
class AccessEntry:
    """Current access entry"""
    user_id: int
    user_email: str
    user_name: str
    access_type: str
    access_type_display: str
    granted_by_id: int
    granted_by_name: str
    granted_at: str
    expires_at: Optional[str]


@dataclass
class FormMetadata:
    """Form metadata for report"""
    form_id: int
    form_name: str
    form_description: Optional[str]
    created_by_id: int
    created_by_email: str
    created_by_name: str
    created_at: str
    current_status: str
    current_approval_status: str
    deployment_cost: Optional[float]
    company_id: int
    company_name: str
    event_id: Optional[int]
    event_name: Optional[str]


@dataclass
class FormAuditReport:
    """Complete Form Audit Report for Compliance"""
    report_generated_at: str
    form_metadata: FormMetadata
    approval_chain: List[ApprovalChainEntry]
    current_access_list: List[AccessEntry]
    activity_timeline: List[AuditEntry]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "report_generated_at": self.report_generated_at,
            "form_metadata": asdict(self.form_metadata),
            "approval_chain": [asdict(a) for a in self.approval_chain],
            "current_access_list": [asdict(a) for a in self.current_access_list],
            "activity_timeline": [asdict(a) for a in self.activity_timeline]
        }


@dataclass  
class EventAuditReport:
    """Complete Event Audit Report for Compliance"""
    report_generated_at: str
    event_id: int
    event_name: str
    company_id: int
    company_name: str
    created_by_id: int
    created_by_name: str
    created_at: str
    current_status: str
    forms_count: int
    activity_timeline: List[AuditEntry]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "report_generated_at": self.report_generated_at,
            "event_id": self.event_id,
            "event_name": self.event_name,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "created_by_id": self.created_by_id,
            "created_by_name": self.created_by_name,
            "created_at": self.created_at,
            "current_status": self.current_status,
            "forms_count": self.forms_count,
            "activity_timeline": [asdict(a) for a in self.activity_timeline]
        }


# Action code to display name mapping
ACTION_DISPLAY_MAP = {
    "form.created": "Form Created",
    "form.updated": "Form Updated",
    "form.deleted": "Form Deleted",
    "form.submitted_for_approval": "Submitted for Approval",
    "form.approved": "Approved (Internal)",
    "form.rejected": "Rejected (Internal)",
    "form.approved_external": "Approved (External)",
    "form.rejected_external": "Rejected (External)",
    "form.published": "Form Published",  # Auto-published after approval
    "form.external_approval_requested": "External Approval Requested",
    "form.ownership_transferred": "Ownership Transferred",
    "form.access.granted": "Access Granted",
    "form.access.updated": "Access Updated",
    "form.access.revoked": "Access Revoked",
    "form.status.published": "Form Published",  # Legacy - manual publish
    "form.status.archived": "Form Archived",
    "event.created": "Event Created",
    "event.updated": "Event Updated",
    "event.deleted": "Event Deleted",
    "event.status.approved": "Event Approved",
    "event.status.rejected": "Event Rejected",
    "event.status.published": "Event Published"
}


class ComplianceService:
    """Service for generating compliance and audit reports"""
    
    def __init__(self, db: Session):
        self.db = db
        # Cache for ID to name lookups
        self._status_cache = {}
        self._approval_status_cache = {}
        self._event_cache = {}
    
    def _get_form_status_name(self, status_id: int) -> str:
        """Get form status name from ID, with caching"""
        if status_id not in self._status_cache:
            status = self.db.get(FormStatus, status_id)
            self._status_cache[status_id] = status.StatusName if status else f"Status {status_id}"
        return self._status_cache[status_id]
    
    def _get_approval_status_name(self, status_id: int) -> str:
        """Get form approval status name from ID, with caching"""
        if status_id not in self._approval_status_cache:
            status = self.db.get(FormApprovalStatus, status_id)
            self._approval_status_cache[status_id] = status.StatusName if status else f"Approval Status {status_id}"
        return self._approval_status_cache[status_id]
    
    def _get_event_name(self, event_id: int) -> str:
        """Get event name from ID, with caching"""
        if event_id not in self._event_cache:
            event = self.db.get(Event, event_id)
            self._event_cache[event_id] = event.Name if event else f"Event {event_id}"
        return self._event_cache[event_id]
    
    def _translate_value_json(self, json_str: Optional[str]) -> Optional[str]:
        """
        Translate IDs in JSON values to human-readable names.
        Handles old log entries that have raw IDs like form_status_id, form_approval_status_id, etc.
        """
        if not json_str:
            return json_str
            
        try:
            data = json.loads(json_str)
            if not isinstance(data, dict):
                return json_str
                
            translated = {}
            for key, value in data.items():
                # Translate form_status_id to Status
                if key == 'form_status_id' and isinstance(value, int):
                    translated['Status'] = self._get_form_status_name(value)
                # Translate form_approval_status_id to Approval Status  
                elif key == 'form_approval_status_id' and isinstance(value, int):
                    translated['Approval Status'] = self._get_approval_status_name(value)
                # Translate event_id to Event
                elif key == 'event_id' and isinstance(value, int):
                    translated['Event'] = self._get_event_name(value)
                # Clean up field names (form_name -> Form Name, etc.)
                elif key == 'form_name':
                    translated['Form Name'] = value
                elif key == 'form_description':
                    translated['Description'] = value
                elif key == 'deployment_cost':
                    translated['Deployment Cost'] = f"${value:.2f}" if value else value
                elif key == 'is_public':
                    translated['Public'] = 'Yes' if value else 'No'
                # Skip internal fields
                elif key in ('details', 'changes', 'updated_by', 'created_by', 'form_id', 'company_id', 'user_id'):
                    continue
                # Keep other fields with cleaned names
                else:
                    clean_key = key.replace('_', ' ').title()
                    translated[clean_key] = value
                    
            return json.dumps(translated) if translated else json_str
        except (json.JSONDecodeError, Exception):
            return json_str

    async def generate_form_audit_report(self, form_id: int) -> FormAuditReport:
        """
        Generate a comprehensive audit report for a specific form.
        
        Includes:
        - Form metadata (creator, dates, status)
        - Approval chain (who approved, when, including external approvers)
        - Current access list (who can view/edit)
        - Complete activity timeline
        
        Args:
            form_id: The form ID to generate report for
            
        Returns:
            FormAuditReport with all compliance data
            
        Raises:
            ValueError: If form not found
        """
        # 1. Get form with relationships
        form = self.db.execute(
            select(Form)
            .options(
                joinedload(Form.form_status),
                joinedload(Form.form_approval_status),
                joinedload(Form.company),
                joinedload(Form.event),
                joinedload(Form.created_by_user)
            )
            .where(Form.FormID == form_id)
        ).scalar_one_or_none()
        
        if not form:
            raise ValueError(f"Form not found: {form_id}")
            
        # 2. Build form metadata
        creator = form.created_by_user if form.created_by_user else self.db.get(User, form.CreatedBy)
        creator_name = f"{creator.FirstName} {creator.LastName}" if creator else "Unknown"
        creator_email = creator.Email if creator else "unknown@unknown.com"
        
        company_name = form.company.CompanyName if form.company else "Unknown"
        event_name = form.event.Name if form.event else None
        
        form_metadata = FormMetadata(
            form_id=form.FormID,
            form_name=form.FormName,
            form_description=form.FormDescription,
            created_by_id=form.CreatedBy,
            created_by_email=creator_email,
            created_by_name=creator_name,
            created_at=to_utc_iso(form.CreatedDate),
            current_status=form.form_status.StatusName if form.form_status else "Unknown",
            current_approval_status=form.form_approval_status.ApprovalStatusName if form.form_approval_status else "Unknown",
            deployment_cost=float(form.DeploymentCost) if form.DeploymentCost else None,
            company_id=form.CompanyID,
            company_name=company_name,
            event_id=form.EventID,
            event_name=event_name
        )
        
        # 3. Build approval chain
        approval_chain = await self._build_approval_chain(form_id)
        
        # 4. Build current access list
        current_access_list = await self._build_access_list(form_id)
        
        # 5. Build activity timeline
        activity_timeline = await self._build_activity_timeline("Form", form_id)
        
        return FormAuditReport(
            report_generated_at=to_utc_iso(datetime.utcnow()),
            form_metadata=form_metadata,
            approval_chain=approval_chain,
            current_access_list=current_access_list,
            activity_timeline=activity_timeline
        )

    async def generate_event_audit_report(self, event_id: int) -> EventAuditReport:
        """
        Generate a comprehensive audit report for a specific event.
        
        Includes:
        - Event metadata
        - Form count
        - Complete activity timeline
        
        Args:
            event_id: The event ID to generate report for
            
        Returns:
            EventAuditReport with all compliance data
            
        Raises:
            ValueError: If event not found
        """
        # 1. Get event with relationships
        event = self.db.execute(
            select(Event)
            .options(
                joinedload(Event.company),
                joinedload(Event.event_status),
                joinedload(Event.created_by_user)
            )
            .where(Event.EventID == event_id)
        ).scalar_one_or_none()
        
        if not event:
            raise ValueError(f"Event not found: {event_id}")
            
        # 2. Get form count
        forms_count = self.db.execute(
            select(Form.FormID)
            .where(Form.EventID == event_id, Form.IsDeleted == False)
        ).scalars().all()
        
        # 3. Build activity timeline
        activity_timeline = await self._build_activity_timeline("Event", event_id)
        
        # Also include form activities for this event
        for form_id in forms_count:
            form_activities = await self._build_activity_timeline("Form", form_id)
            activity_timeline.extend(form_activities)
        
        # Sort combined timeline by timestamp descending
        activity_timeline.sort(key=lambda x: x.timestamp, reverse=True)
        
        creator = event.created_by_user if event.created_by_user else self.db.get(User, event.CreatedBy)
        creator_name = f"{creator.FirstName} {creator.LastName}" if creator else "Unknown"
        company_name = event.company.CompanyName if event.company else "Unknown"
        
        return EventAuditReport(
            report_generated_at=to_utc_iso(datetime.utcnow()),
            event_id=event.EventID,
            event_name=event.Name,
            company_id=event.CompanyID,
            company_name=company_name,
            created_by_id=event.CreatedBy,
            created_by_name=creator_name,
            created_at=to_utc_iso(event.CreatedDate),
            current_status=event.event_status.StatusName if event.event_status else "Unknown",
            forms_count=len(forms_count),
            activity_timeline=activity_timeline
        )

    async def get_company_activity_log(
        self, 
        company_id: Optional[int] = None, 
        page: int = 1, 
        page_size: int = 50,
        entity_type: str = None,
        action_filter: str = None,
        user_id_filter: Optional[int] = None,
        form_id_filter: Optional[int] = None,
        event_id_filter: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get paginated activity log for a company or all companies.
        
        Args:
            company_id: Company ID (None = all companies, for System Admins)
            page: Page number (1-based)
            page_size: Items per page
            entity_type: Optional filter by entity type (Form, Event, etc.)
            action_filter: Optional filter by action code
            user_id_filter: Optional filter by user ID
            form_id_filter: Optional filter by form ID (EntityID where EntityType=Form)
            event_id_filter: Optional filter by event ID (EntityID where EntityType=Event)
            
        Returns:
            Dictionary with items and pagination info
        """
        from models.company import Company
        from models.form import Form
        from models.event import Event
        from sqlalchemy import func, or_
        
        # Start with base query
        query = select(ActivityLog).order_by(ActivityLog.CreatedDate.desc())
        
        # Filter by company if specified (None = all companies for System Admin)
        if company_id is not None:
            query = query.where(ActivityLog.CompanyID == company_id)
        
        # Apply filters
        if entity_type:
            query = query.where(ActivityLog.EntityType == entity_type)
        if action_filter:
            query = query.where(ActivityLog.Action.like(f"%{action_filter}%"))
        if user_id_filter:
            query = query.where(ActivityLog.UserID == user_id_filter)
        if form_id_filter:
            query = query.where(
                ActivityLog.EntityType == "Form",
                ActivityLog.EntityID == form_id_filter
            )
        if event_id_filter:
            # For events, check both direct Event logs and Form logs associated with the event
            # Get all form IDs for this event
            form_ids_subquery = select(Form.FormID).where(Form.EventID == event_id_filter)
            query = query.where(
                or_(
                    # Direct event logs
                    (ActivityLog.EntityType == "Event") & (ActivityLog.EntityID == event_id_filter),
                    # Form logs for forms belonging to this event
                    (ActivityLog.EntityType == "Form") & (ActivityLog.EntityID.in_(form_ids_subquery))
                )
            )
            
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_count = self.db.execute(count_query).scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        logs = self.db.execute(query).scalars().all()
        
        # Build lookup caches to avoid N+1 queries
        company_cache: Dict[int, str] = {}
        form_cache: Dict[int, tuple] = {}  # form_id -> (form_name, event_name)
        event_cache: Dict[int, str] = {}
        
        # Convert to AuditEntry format
        items = []
        for log in logs:
            # Try to get user name
            user_name = None
            is_external = False
            if log.UserID:
                user = self.db.get(User, log.UserID)
                if user:
                    user_name = f"{user.FirstName} {user.LastName}"
                    # Check if external user
                    from models.ref.user_status import UserStatus
                    status = self.db.get(UserStatus, user.StatusID)
                    is_external = status and status.StatusCode == 'EXTERNAL'
            
            # Get company name
            company_name = None
            if log.CompanyID:
                if log.CompanyID not in company_cache:
                    company = self.db.get(Company, log.CompanyID)
                    company_cache[log.CompanyID] = company.CompanyName if company else None
                company_name = company_cache.get(log.CompanyID)
            
            # Get form/event names based on entity type
            form_name = None
            event_name = None
            
            if log.EntityType == "Form" and log.EntityID:
                if log.EntityID not in form_cache:
                    form = self.db.get(Form, log.EntityID)
                    if form:
                        form_cache[log.EntityID] = (form.FormName, None)
                        # Also get event name if form has event
                        if form.EventID:
                            if form.EventID not in event_cache:
                                event = self.db.get(Event, form.EventID)
                                event_cache[form.EventID] = event.Name if event else None
                            form_cache[log.EntityID] = (form.FormName, event_cache.get(form.EventID))
                    else:
                        form_cache[log.EntityID] = (None, None)
                form_name, event_name = form_cache.get(log.EntityID, (None, None))
                
            elif log.EntityType == "Event" and log.EntityID:
                if log.EntityID not in event_cache:
                    event = self.db.get(Event, log.EntityID)
                    event_cache[log.EntityID] = event.Name if event else None
                event_name = event_cache.get(log.EntityID)
                    
            # Parse details from NewValue if JSON
            details = log.NewValue
            token_id = None
            if details and details.startswith('{'):
                try:
                    parsed = json.loads(details)
                    details = parsed.get('details', details)
                    token_id = parsed.get('approval_token_id')
                except:
                    pass
                    
            items.append(AuditEntry(
                timestamp=to_utc_iso(log.CreatedDate),
                action=log.Action,
                action_display=ACTION_DISPLAY_MAP.get(log.Action, log.Action),
                user_id=log.UserID,
                user_email=log.UserEmail,
                user_name=user_name,
                is_external=is_external,
                details=details,
                old_value=log.OldValue,
                new_value=log.NewValue,
                token_id=token_id,
                company_id=log.CompanyID,
                company_name=company_name,
                entity_id=log.EntityID,
                entity_type=log.EntityType,
                form_name=form_name,
                event_name=event_name
            ))
            
        return {
            "items": [asdict(item) for item in items],
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size
        }

    async def _build_approval_chain(self, form_id: int) -> List[ApprovalChainEntry]:
        """Build the approval chain for a form from tokens and logs"""
        chain = []
        
        # Get all approval tokens for this form
        tokens = self.db.execute(
            select(FormApprovalToken)
            .where(FormApprovalToken.FormID == form_id)
            .order_by(FormApprovalToken.CreatedDate)
        ).scalars().all()
        
        for token in tokens:
            # Find the decision log entry if used
            decision = "Pending"
            decided_at = None
            reason = None
            
            if token.IsUsed:
                # Find the approval/rejection log
                decision_log = self.db.execute(
                    select(ActivityLog)
                    .where(
                        ActivityLog.EntityType == "Form",
                        ActivityLog.EntityID == form_id,
                        or_(
                            ActivityLog.Action == "form.approved_external",
                            ActivityLog.Action == "form.rejected_external"
                        ),
                        ActivityLog.UserID == token.UserID
                    )
                    .order_by(ActivityLog.CreatedDate.desc())
                ).scalar_one_or_none()
                
                if decision_log:
                    decision = "Approved" if "approved" in decision_log.Action else "Rejected"
                    decided_at = to_utc_iso(decision_log.CreatedDate)
                    
                    # Try to extract reason
                    if decision_log.NewValue:
                        try:
                            parsed = json.loads(decision_log.NewValue)
                            if "Reason:" in parsed.get('details', ''):
                                reason = parsed['details'].split("Reason:")[-1].strip()
                        except:
                            if "Reason:" in str(decision_log.NewValue):
                                reason = str(decision_log.NewValue).split("Reason:")[-1].strip()
                                
            # Get approver name
            approver_name = None
            if token.UserID:
                user = self.db.get(User, token.UserID)
                if user:
                    approver_name = f"{user.FirstName} {user.LastName}"
                    
            chain.append(ApprovalChainEntry(
                approver_id=token.UserID,
                approver_email=token.Email,
                approver_name=approver_name,
                is_external=True,
                decision=decision,
                decided_at=decided_at,
                token_id=token.FormApprovalTokenID,
                reason=reason
            ))
            
        # Also check for internal approvals
        internal_approvals = self.db.execute(
            select(ActivityLog)
            .where(
                ActivityLog.EntityType == "Form",
                ActivityLog.EntityID == form_id,
                or_(
                    ActivityLog.Action == "form.approved",
                    ActivityLog.Action == "form.rejected"
                )
            )
            .order_by(ActivityLog.CreatedDate)
        ).scalars().all()
        
        for log in internal_approvals:
            user = self.db.get(User, log.UserID) if log.UserID else None
            user_name = f"{user.FirstName} {user.LastName}" if user else "Unknown"
            user_email = user.Email if user else None
            
            reason = None
            if log.NewValue and "Reason:" in str(log.NewValue):
                reason = str(log.NewValue).split("Reason:")[-1].strip()
                
            chain.append(ApprovalChainEntry(
                approver_id=log.UserID,
                approver_email=user_email,
                approver_name=user_name,
                is_external=False,
                decision="Approved" if "approved" in log.Action else "Rejected",
                decided_at=to_utc_iso(log.CreatedDate),
                token_id=None,
                reason=reason
            ))
            
        return chain

    async def _build_access_list(self, form_id: int) -> List[AccessEntry]:
        """Build current access list for a form"""
        access_entries = []
        
        # Get active access control entries
        access_controls = self.db.execute(
            select(FormAccessControl)
            .options(
                joinedload(FormAccessControl.user),
                joinedload(FormAccessControl.access_type),
                joinedload(FormAccessControl.granted_by_user)
            )
            .where(
                FormAccessControl.FormID == form_id,
                FormAccessControl.IsDeleted == False
            )
        ).scalars().unique().all()
        
        for ac in access_controls:
            user = ac.user
            granted_by = ac.granted_by_user
            access_type = ac.access_type
            
            access_entries.append(AccessEntry(
                user_id=ac.UserID,
                user_email=user.Email if user else "unknown@unknown.com",
                user_name=f"{user.FirstName} {user.LastName}" if user else "Unknown",
                access_type=access_type.AccessTypeCode if access_type else "UNKNOWN",
                access_type_display=access_type.AccessTypeName if access_type else "Unknown",
                granted_by_id=ac.GrantedBy,
                granted_by_name=f"{granted_by.FirstName} {granted_by.LastName}" if granted_by else "Unknown",
                granted_at=to_utc_iso(ac.GrantedDate),
                expires_at=to_utc_iso(ac.ExpiryDate)
            ))
            
        return access_entries

    async def _build_activity_timeline(
        self, 
        entity_type: str, 
        entity_id: int
    ) -> List[AuditEntry]:
        """Build activity timeline for an entity"""
        entries = []
        
        logs = self.db.execute(
            select(ActivityLog)
            .where(
                ActivityLog.EntityType == entity_type,
                ActivityLog.EntityID == entity_id
            )
            .order_by(ActivityLog.CreatedDate.desc())
        ).scalars().all()
        
        for log in logs:
            # Get user info
            user = self.db.get(User, log.UserID) if log.UserID else None
            user_name = f"{user.FirstName} {user.LastName}" if user else None
            
            # Check if external
            is_external = False
            if user:
                from models.ref.user_status import UserStatus
                status = self.db.get(UserStatus, user.StatusID)
                is_external = status and status.StatusCode == 'EXTERNAL'
                
            # Parse NewValue for details and token_id
            details = log.NewValue
            token_id = None
            if details and details.startswith('{'):
                try:
                    parsed = json.loads(details)
                    details = parsed.get('details', details)
                    token_id = parsed.get('approval_token_id') or parsed.get('token_id')
                except:
                    pass
            
            # Translate IDs to human-readable names in old/new values
            translated_old = self._translate_value_json(log.OldValue)
            translated_new = self._translate_value_json(log.NewValue)
                    
            entries.append(AuditEntry(
                timestamp=to_utc_iso(log.CreatedDate),
                action=log.Action,
                action_display=ACTION_DISPLAY_MAP.get(log.Action, log.Action),
                user_id=log.UserID,
                user_email=log.UserEmail or (user.Email if user else None),
                user_name=user_name,
                is_external=is_external,
                details=details,
                old_value=translated_old,
                new_value=translated_new,
                token_id=token_id
            ))
            
        return entries

