"""
UserPreference Model (dbo.UserPreference)
Per-user preference values — one row per user × preference key.

The model only stores overrides. When no row exists for a user × key,
the read API returns ref.UserPreferenceKey.DefaultValue instead.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserPreference(Base):
    """
    Per-user preference override storage.

    Rows materialise naturally on first user override — no backfill required
    because the read API falls back to ref.UserPreferenceKey.DefaultValue
    when no row exists for a given user × preference key combination.

    Attributes:
        UserPreferenceID: Primary key
        UserID: FK → dbo.User.UserID (indexed)
        PreferenceKeyID: FK → ref.UserPreferenceKey.UserPreferenceKeyID (indexed)
        PreferenceValue: Stored as string; type-converted on read using SettingType
        Unique constraint on (UserID, PreferenceKeyID) — one override per user per key
    """

    __tablename__ = "UserPreference"
    __table_args__ = (
        UniqueConstraint("UserID", "PreferenceKeyID", name="UQ_UserPreference_UserID_PreferenceKeyID"),
        {"schema": "dbo"},
    )

    UserPreferenceID = Column(BigInteger, primary_key=True, autoincrement=True)

    UserID = Column(
        BigInteger,
        ForeignKey("dbo.User.UserID"),
        nullable=False,
        index=True,
    )
    PreferenceKeyID = Column(
        BigInteger,
        ForeignKey("ref.UserPreferenceKey.UserPreferenceKeyID"),
        nullable=False,
        index=True,
    )
    PreferenceValue = Column(String(None), nullable=False)  # NVARCHAR(MAX)

    # Full audit columns — matches dbo.User / config.AppSetting pattern
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, nullable=True)

    # Relationships
    user = relationship("User", back_populates="user_preferences", foreign_keys=[UserID])
    preference_key = relationship("UserPreferenceKey", back_populates="user_preferences")

    def __repr__(self) -> str:
        return (
            f"<UserPreference("
            f"UserPreferenceID={self.UserPreferenceID}, "
            f"UserID={self.UserID}, "
            f"PreferenceKeyID={self.PreferenceKeyID}, "
            f"PreferenceValue='{self.PreferenceValue}')>"
        )
