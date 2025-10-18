"""
Tests for Story 1.11: Company Relationships
Tests relationship creation, circular prevention, and duplicate prevention.
"""
import pytest
from sqlalchemy.orm import Session
from modules.companies.relationship_service import RelationshipService
from models.company import Company
from models.user import User
from models.company_relationship import CompanyRelationship
from models.ref.company_relationship_type import CompanyRelationshipType


@pytest.fixture
def relationship_service(db_session: Session):
    return RelationshipService(db_session)


@pytest.fixture
def test_companies(db_session: Session, test_user: User):
    """Create test companies for relationship testing."""
    from models.ref.country import Country
    
    # Get a valid CountryID (required field)
    country = db_session.query(Country).first()
    if not country:
        # Create a test country if none exists
        country = Country(
            CountryName='Australia',
            CountryCode='AU',
            IsActive=True
        )
        db_session.add(country)
        db_session.commit()
        db_session.refresh(country)
    
    companies = []
    for i in range(5):
        company = Company(
            CompanyName=f"Test Company {i}",
            CountryID=country.CountryID,
            IsActive=True,
            CreatedBy=test_user.UserID,
            UpdatedBy=test_user.UserID
        )
        db_session.add(company)
        companies.append(company)
    
    db_session.commit()
    for company in companies:
        db_session.refresh(company)
    
    return companies


class TestRelationshipCreation:
    """Test creating company relationships."""

    def test_create_branch_relationship(self, relationship_service, test_companies, test_user):
        """Test creating a branch relationship between two companies."""
        parent = test_companies[0]
        child = test_companies[1]
        
        relationship = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        assert relationship.ParentCompanyID == parent.CompanyID
        assert relationship.ChildCompanyID == child.CompanyID
        assert relationship.Status == 'active'
        assert relationship.EstablishedBy == test_user.UserID

    def test_create_subsidiary_relationship(self, relationship_service, test_companies, test_user):
        """Test creating a subsidiary relationship."""
        parent = test_companies[0]
        child = test_companies[2]
        
        relationship = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='subsidiary',
            established_by_user=test_user
        )
        
        assert relationship.ParentCompanyID == parent.CompanyID
        assert relationship.ChildCompanyID == child.CompanyID
        assert relationship.Status == 'active'

    def test_create_partner_relationship(self, relationship_service, test_companies, test_user):
        """Test creating a partner relationship."""
        company_a = test_companies[0]
        company_b = test_companies[3]
        
        relationship = relationship_service.create_relationship(
            parent_id=company_a.CompanyID,
            child_id=company_b.CompanyID,
            relationship_type_name='partner',
            established_by_user=test_user
        )
        
        assert relationship.ParentCompanyID == company_a.CompanyID
        assert relationship.ChildCompanyID == company_b.CompanyID


class TestRelationshipValidations:
    """Test relationship validation rules."""

    def test_prevent_self_relationship(self, relationship_service, test_companies, test_user):
        """Test that a company cannot have a relationship with itself."""
        company = test_companies[0]
        
        with pytest.raises(ValueError, match="cannot have a relationship with itself"):
            relationship_service.create_relationship(
                parent_id=company.CompanyID,
                child_id=company.CompanyID,
                relationship_type_name='branch',
                established_by_user=test_user
            )

    def test_prevent_duplicate_relationship(self, relationship_service, test_companies, test_user):
        """Test that duplicate relationships are prevented."""
        parent = test_companies[0]
        child = test_companies[1]
        
        # Create first relationship
        relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Try to create duplicate
        with pytest.raises(ValueError, match="relationship already exists"):
            relationship_service.create_relationship(
                parent_id=parent.CompanyID,
                child_id=child.CompanyID,
                relationship_type_name='subsidiary',
                established_by_user=test_user
            )

    def test_prevent_circular_relationship_simple(self, relationship_service, test_companies, test_user):
        """Test prevention of simple circular relationship (A -> B -> A)."""
        company_a = test_companies[0]
        company_b = test_companies[1]
        
        # Create A -> B
        relationship_service.create_relationship(
            parent_id=company_a.CompanyID,
            child_id=company_b.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Try to create B -> A (circular) - service catches this as "already exists" (bidirectional check)
        with pytest.raises(ValueError, match="already exists"):
            relationship_service.create_relationship(
                parent_id=company_b.CompanyID,
                child_id=company_a.CompanyID,
                relationship_type_name='branch',
                established_by_user=test_user
            )

    def test_prevent_circular_relationship_complex(self, relationship_service, test_companies, test_user):
        """Test prevention of complex circular relationship (A -> B -> C -> A)."""
        company_a = test_companies[0]
        company_b = test_companies[1]
        company_c = test_companies[2]
        
        # Create A -> B -> C
        relationship_service.create_relationship(
            parent_id=company_a.CompanyID,
            child_id=company_b.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        relationship_service.create_relationship(
            parent_id=company_b.CompanyID,
            child_id=company_c.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Try to create C -> A (circular)
        with pytest.raises(ValueError, match="circular dependency"):
            relationship_service.create_relationship(
                parent_id=company_c.CompanyID,
                child_id=company_a.CompanyID,
                relationship_type_name='branch',
                established_by_user=test_user
            )

    def test_invalid_relationship_type(self, relationship_service, test_companies, test_user):
        """Test that invalid relationship types are rejected."""
        parent = test_companies[0]
        child = test_companies[1]
        
        with pytest.raises(ValueError, match="Invalid relationship type"):
            relationship_service.create_relationship(
                parent_id=parent.CompanyID,
                child_id=child.CompanyID,
                relationship_type_name='invalid_type',
                established_by_user=test_user
            )


class TestRelationshipQueries:
    """Test querying relationships."""

    def test_get_relationship_between(self, relationship_service, test_companies, test_user):
        """Test finding relationship between two companies."""
        parent = test_companies[0]
        child = test_companies[1]
        
        # Create relationship
        created = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Query in both directions
        found = relationship_service.get_relationship_between(parent.CompanyID, child.CompanyID)
        assert found is not None
        assert found.CompanyRelationshipID == created.CompanyRelationshipID
        
        found_reverse = relationship_service.get_relationship_between(child.CompanyID, parent.CompanyID)
        assert found_reverse is not None
        assert found_reverse.CompanyRelationshipID == created.CompanyRelationshipID

    def test_get_company_relationships(self, relationship_service, test_companies, test_user):
        """Test getting all relationships for a company."""
        parent = test_companies[0]
        child1 = test_companies[1]
        child2 = test_companies[2]
        
        # Create multiple relationships
        relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child1.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child2.CompanyID,
            relationship_type_name='subsidiary',
            established_by_user=test_user
        )
        
        # Get all relationships for parent
        relationships = relationship_service.get_company_relationships(parent.CompanyID)
        assert len(relationships) == 2


class TestRelationshipStatusUpdates:
    """Test updating relationship status."""

    def test_suspend_relationship(self, relationship_service, test_companies, test_user):
        """Test suspending a relationship."""
        parent = test_companies[0]
        child = test_companies[1]
        
        # Create relationship
        relationship = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Suspend it
        updated = relationship_service.update_relationship_status(
            relationship_id=relationship.CompanyRelationshipID,
            status='suspended',
            updated_by_user=test_user
        )
        
        assert updated.Status == 'suspended'

    def test_terminate_relationship(self, relationship_service, test_companies, test_user):
        """Test terminating a relationship."""
        parent = test_companies[0]
        child = test_companies[1]
        
        # Create relationship
        relationship = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Terminate it
        updated = relationship_service.update_relationship_status(
            relationship_id=relationship.CompanyRelationshipID,
            status='terminated',
            updated_by_user=test_user
        )
        
        assert updated.Status == 'terminated'

    def test_invalid_status_update(self, relationship_service, test_companies, test_user):
        """Test that invalid status updates are rejected."""
        parent = test_companies[0]
        child = test_companies[1]
        
        # Create relationship
        relationship = relationship_service.create_relationship(
            parent_id=parent.CompanyID,
            child_id=child.CompanyID,
            relationship_type_name='branch',
            established_by_user=test_user
        )
        
        # Try invalid status
        with pytest.raises(ValueError, match="Invalid status"):
            relationship_service.update_relationship_status(
                relationship_id=relationship.CompanyRelationshipID,
                status='invalid_status',
                updated_by_user=test_user
            )

