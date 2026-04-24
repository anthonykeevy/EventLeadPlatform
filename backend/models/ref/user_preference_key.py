"""
UserPreferenceKey Reference Model (ref.UserPreferenceKey)
Catalogue of available user preferences — mirrors config.AppSetting columns.

Reuses ref.SettingType for type coercion (no parallel type system).
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserPreferenceKey(Base):
    """
    User preference key catalogue.

    Each row defines one preference: its type, default value, display metadata,
    and validation rules. A UserPreference row only materialises when the user
    overrides the default — new users see DefaultValue without any rows.

    Attributes:
        UserPreferenceKeyID: Primary key
        PreferenceKey: Unique dot-namespaced key (e.g. 'notifications.ai_agent.suppress_replace_warning')
        PreferenceCategoryID: FK → ref.UserPreferenceCategory
        SettingTypeID: FK → ref.SettingType (REUSE — no parallel type system)
        DisplayName: Human-readable label shown in the Preferences UI
        Description: Help text displayed under the control
        DefaultValue: Used when no UserPreference row exists for the user
        IsEditable: Allow disabling user override (rare but useful)
        IsActive: Soft-disable a preference without dropping the row
        SortOrder: Order within the category in the Preferences UI
    """

    __tablename__ = "UserPreferenceKey"
    __table_args__ = {"schema": "ref"}

    UserPreferenceKeyID = Column(BigInteger, primary_key=True, autoincrement=True)

    PreferenceKey = Column(String(150), nullable=False, unique=True)
    DisplayName = Column(String(200), nullable=False)
    Description = Column(String(500), nullable=False, default="")
    DefaultValue = Column(String(None), nullable=False)  # NVARCHAR(MAX)

    PreferenceCategoryID = Column(
        BigInteger,
        ForeignKey("ref.UserPreferenceCategory.UserPreferenceCategoryID"),
        nullable=False,
        index=True,
    )
    SettingTypeID = Column(
        BigInteger,
        ForeignKey("ref.SettingType.SettingTypeID"),
        nullable=False,
        index=True,
    )

    IsEditable = Column(Boolean, nullable=False, default=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=999)

    # Audit columns — minimal for reference tables
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, nullable=True)

    # Relationships
    category = relationship("UserPreferenceCategory", back_populates="preference_keys")
    setting_type = relationship("SettingType", back_populates="user_preference_keys")
    user_preferences = relationship("UserPreference", back_populates="preference_key")

    def __repr__(self) -> str:
        return (
            f"<UserPreferenceKey("
            f"UserPreferenceKeyID={self.UserPreferenceKeyID}, "
            f"PreferenceKey='{self.PreferenceKey}')>"
        )
