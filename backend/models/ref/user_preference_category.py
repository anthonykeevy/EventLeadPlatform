"""
UserPreferenceCategory Reference Model (ref.UserPreferenceCategory)
Categories for user preferences — mirrors the ref.SettingCategory pattern.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserPreferenceCategory(Base):
    """
    User preference category reference table.

    Groups user preferences for display in the Preferences UI.
    Categories: Notifications, Theme, Account, AI Agent, ...

    Attributes:
        UserPreferenceCategoryID: Primary key
        CategoryName: Display name (unique, e.g. 'Notifications')
        Description: Displayed as section header copy in the Preferences UI
        DisplayOrder: Sort order across categories
        IsActive: Hide a category without dropping it
    """

    __tablename__ = "UserPreferenceCategory"
    __table_args__ = {"schema": "ref"}

    UserPreferenceCategoryID = Column(BigInteger, primary_key=True, autoincrement=True)

    CategoryName = Column(String(100), nullable=False, unique=True)
    Description = Column(String(500), nullable=False, default="")
    DisplayOrder = Column(Integer, nullable=False, default=999)
    IsActive = Column(Boolean, nullable=False, default=True)

    # Audit columns — minimal for reference tables (matches ref.SettingCategory)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, nullable=True)

    # Relationships
    preference_keys = relationship("UserPreferenceKey", back_populates="category")

    def __repr__(self) -> str:
        return (
            f"<UserPreferenceCategory("
            f"UserPreferenceCategoryID={self.UserPreferenceCategoryID}, "
            f"CategoryName='{self.CategoryName}')>"
        )
