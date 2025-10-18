"""
Service for managing company relationships.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from datetime import datetime
import logging

from models.company import Company
from models.company_relationship import CompanyRelationship
from models.ref.company_relationship_type import CompanyRelationshipType
from models.user import User

logger = logging.getLogger(__name__)


class RelationshipService:
    def __init__(self, db: Session):
        self.db = db

    def get_relationship_between(self, company_a_id: int, company_b_id: int) -> Optional[CompanyRelationship]:
        """
        Checks if a relationship exists between two companies, in either direction.
        """
        stmt = select(CompanyRelationship).where(
            or_(
                (CompanyRelationship.ParentCompanyID == company_a_id) & (CompanyRelationship.ChildCompanyID == company_b_id),
                (CompanyRelationship.ParentCompanyID == company_b_id) & (CompanyRelationship.ChildCompanyID == company_a_id)
            )
        )
        return self.db.execute(stmt).scalars().first()

    def _is_circular_relationship(self, parent_id: int, child_id: int) -> bool:
        """
        Detects if creating a relationship would result in a circular dependency.
        (e.g., A -> B -> C, then trying to create C -> A)
        """
        ancestor_id = parent_id
        while ancestor_id is not None:
            if ancestor_id == child_id:
                return True
            
            stmt = select(CompanyRelationship.ParentCompanyID).where(CompanyRelationship.ChildCompanyID == ancestor_id)
            ancestor_id = self.db.execute(stmt).scalars().first()
        
        return False

    def create_relationship(
        self,
        parent_id: int,
        child_id: int,
        relationship_type_name: str,
        established_by_user: User
    ) -> CompanyRelationship:
        """
        Establishes a new relationship between two companies.
        """
        # Validation: Ensure companies are not the same
        if parent_id == child_id:
            raise ValueError("A company cannot have a relationship with itself.")

        # Validation: Check for existing relationship
        if self.get_relationship_between(parent_id, child_id):
            raise ValueError("A relationship already exists between these two companies.")

        # Validation: Check for circular dependency
        if self._is_circular_relationship(parent_id, child_id):
            raise ValueError("This relationship would create a circular dependency.")
            
        # Get relationship type ID from name
        stmt = select(CompanyRelationshipType.CompanyRelationshipTypeID).where(CompanyRelationshipType.TypeName == relationship_type_name)
        relationship_type_id = self.db.execute(stmt).scalars().first()
        if not relationship_type_id:
            raise ValueError(f"Invalid relationship type: {relationship_type_name}")

        new_relationship = CompanyRelationship(
            ParentCompanyID=parent_id,
            ChildCompanyID=child_id,
            RelationshipTypeID=relationship_type_id,
            Status='active',
            EstablishedBy=established_by_user.UserID,
            CreatedBy=established_by_user.UserID,
            UpdatedBy=established_by_user.UserID,
        )
        
        self.db.add(new_relationship)
        self.db.commit()
        self.db.refresh(new_relationship)
        
        return new_relationship

    def get_company_relationships(self, company_id: int) -> List[CompanyRelationship]:
        """
        Gets all relationships (parent and child) for a given company.
        """
        stmt = select(CompanyRelationship).where(
            or_(
                CompanyRelationship.ParentCompanyID == company_id,
                CompanyRelationship.ChildCompanyID == company_id
            )
        )
        return self.db.execute(stmt).scalars().all()

    def update_relationship_status(
        self,
        relationship_id: int,
        status: str,
        updated_by_user: User
    ) -> CompanyRelationship:
        """
        Updates the status of an existing relationship (e.g., to 'suspended' or 'terminated').
        """
        allowed_statuses = {'active', 'suspended', 'terminated'}
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status. Must be one of {allowed_statuses}")

        relationship = self.db.get(CompanyRelationship, relationship_id)
        if not relationship:
            raise ValueError("Relationship not found.")

        relationship.Status = status
        relationship.UpdatedBy = updated_by_user.UserID
        relationship.UpdatedDate = datetime.utcnow()

        self.db.add(relationship)
        self.db.commit()
        self.db.refresh(relationship)

        logger.info(
            f"Relationship status updated: RelationshipID={relationship_id}, "
            f"NewStatus={status}, UpdatedBy={updated_by_user.UserID}"
        )
        # TODO: Log status change to audit log with reason
        
        return relationship
