"""KB DocRef NULL-safe uniqueness and audit semantics support

Revision ID: 037
Revises: 036
Create Date: 2026-02-09

Purpose:
- Fix DocRef uniqueness expectations in SQL Server:
  - UNIQUE constraints allow multiple rows with NULL key parts; application logic treats
    NULLs as equal (NULL-safe match), so DB must enforce the same semantics.
  - Soft delete semantics require uniqueness among active rows only (IsDeleted = 0).

Approach:
- Drop the original UNIQUE constraint on (DocPath, AnchorID, SnapshotCommitSHA).
- Create four filtered UNIQUE indexes that cover each NULL pattern, filtered to IsDeleted = 0.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "037"
down_revision = "036"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Best-effort de-dupe of active rows that would violate the new filtered unique indexes.
    # This should be a no-op in normal operation, but protects upgrades if duplicates already exist.
    op.execute(
        """
        ;WITH Ranked AS (
            SELECT
                DocRefID,
                DocPath,
                AnchorID,
                SnapshotCommitSHA,
                ROW_NUMBER() OVER (PARTITION BY DocPath, AnchorID, SnapshotCommitSHA ORDER BY DocRefID) AS rn,
                MIN(DocRefID) OVER (PARTITION BY DocPath, AnchorID, SnapshotCommitSHA) AS KeepDocRefID
            FROM [kb].[DocRef]
            WHERE IsDeleted = 0
        ),
        DupeIds AS (
            SELECT DocRefID AS DupeDocRefID, KeepDocRefID
            FROM Ranked
            WHERE rn > 1
        )
        -- kb.AspectDocRef: delete rows that would become duplicates, then repoint remaining rows
        DELETE adr
        FROM [kb].[AspectDocRef] adr
        JOIN DupeIds di ON adr.DocRefID = di.DupeDocRefID
        WHERE EXISTS (
            SELECT 1
            FROM [kb].[AspectDocRef] adr2
            WHERE adr2.IsDeleted = 0
              AND adr2.AspectID = adr.AspectID
              AND adr2.DocRefID = di.KeepDocRefID
        );

        UPDATE adr
        SET adr.DocRefID = di.KeepDocRefID
        FROM [kb].[AspectDocRef] adr
        JOIN DupeIds di ON adr.DocRefID = di.DupeDocRefID
        WHERE adr.IsDeleted = 0;

        -- kb.IdeaDocRef: delete rows that would become duplicates, then repoint remaining rows
        DELETE idr
        FROM [kb].[IdeaDocRef] idr
        JOIN DupeIds di ON idr.DocRefID = di.DupeDocRefID
        WHERE EXISTS (
            SELECT 1
            FROM [kb].[IdeaDocRef] idr2
            WHERE idr2.IsDeleted = 0
              AND idr2.IdeaID = idr.IdeaID
              AND idr2.DocRefID = di.KeepDocRefID
        );

        UPDATE idr
        SET idr.DocRefID = di.KeepDocRefID
        FROM [kb].[IdeaDocRef] idr
        JOIN DupeIds di ON idr.DocRefID = di.DupeDocRefID
        WHERE idr.IsDeleted = 0;

        -- Soft-delete duplicate DocRefs (keeps history, while enabling active-row uniqueness)
        UPDATE dr
        SET dr.IsDeleted = 1,
            dr.DeletedDate = GETUTCDATE()
        FROM [kb].[DocRef] dr
        JOIN DupeIds di ON dr.DocRefID = di.DupeDocRefID
        WHERE dr.IsDeleted = 0;
        """
    )

    # Drop original unique constraint (NULL semantics mismatch; not IsDeleted-aware)
    op.drop_constraint(
        "UQ_DocRef_DocPath_AnchorID_SnapshotCommitSHA",
        "DocRef",
        type_="unique",
        schema="kb",
    )

    # Create NULL-safe, IsDeleted-aware uniqueness via filtered UNIQUE indexes.
    op.create_index(
        "IX_DocRef_Unique_DocPath_A0_S0",
        "DocRef",
        ["DocPath"],
        unique=True,
        schema="kb",
        mssql_where=sa.text("IsDeleted = 0 AND AnchorID IS NULL AND SnapshotCommitSHA IS NULL"),
    )
    op.create_index(
        "IX_DocRef_Unique_DocPath_AnchorID_S0",
        "DocRef",
        ["DocPath", "AnchorID"],
        unique=True,
        schema="kb",
        mssql_where=sa.text("IsDeleted = 0 AND AnchorID IS NOT NULL AND SnapshotCommitSHA IS NULL"),
    )
    op.create_index(
        "IX_DocRef_Unique_DocPath_A0_SnapshotCommitSHA",
        "DocRef",
        ["DocPath", "SnapshotCommitSHA"],
        unique=True,
        schema="kb",
        mssql_where=sa.text("IsDeleted = 0 AND AnchorID IS NULL AND SnapshotCommitSHA IS NOT NULL"),
    )
    op.create_index(
        "IX_DocRef_Unique_DocPath_AnchorID_SnapshotCommitSHA",
        "DocRef",
        ["DocPath", "AnchorID", "SnapshotCommitSHA"],
        unique=True,
        schema="kb",
        mssql_where=sa.text("IsDeleted = 0 AND AnchorID IS NOT NULL AND SnapshotCommitSHA IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("IX_DocRef_Unique_DocPath_A0_S0", table_name="DocRef", schema="kb")
    op.drop_index("IX_DocRef_Unique_DocPath_AnchorID_S0", table_name="DocRef", schema="kb")
    op.drop_index("IX_DocRef_Unique_DocPath_A0_SnapshotCommitSHA", table_name="DocRef", schema="kb")
    op.drop_index("IX_DocRef_Unique_DocPath_AnchorID_SnapshotCommitSHA", table_name="DocRef", schema="kb")

    # Recreate the original UNIQUE constraint. This requires removing any duplicates across all rows
    # (including IsDeleted=1), because UNIQUE constraints are not filtered by IsDeleted.
    op.execute(
        """
        ;WITH Ranked AS (
            SELECT
                DocRefID,
                DocPath,
                AnchorID,
                SnapshotCommitSHA,
                ROW_NUMBER() OVER (PARTITION BY DocPath, AnchorID, SnapshotCommitSHA ORDER BY DocRefID) AS rn,
                MIN(DocRefID) OVER (PARTITION BY DocPath, AnchorID, SnapshotCommitSHA) AS KeepDocRefID
            FROM [kb].[DocRef]
        ),
        DupeIds AS (
            SELECT DocRefID AS DupeDocRefID, KeepDocRefID
            FROM Ranked
            WHERE rn > 1
        )
        -- Remove link rows that would become duplicates, then repoint remaining rows
        DELETE adr
        FROM [kb].[AspectDocRef] adr
        JOIN DupeIds di ON adr.DocRefID = di.DupeDocRefID
        WHERE EXISTS (
            SELECT 1
            FROM [kb].[AspectDocRef] adr2
            WHERE adr2.AspectID = adr.AspectID
              AND adr2.DocRefID = di.KeepDocRefID
        );

        UPDATE adr
        SET adr.DocRefID = di.KeepDocRefID
        FROM [kb].[AspectDocRef] adr
        JOIN DupeIds di ON adr.DocRefID = di.DupeDocRefID;

        DELETE idr
        FROM [kb].[IdeaDocRef] idr
        JOIN DupeIds di ON idr.DocRefID = di.DupeDocRefID
        WHERE EXISTS (
            SELECT 1
            FROM [kb].[IdeaDocRef] idr2
            WHERE idr2.IdeaID = idr.IdeaID
              AND idr2.DocRefID = di.KeepDocRefID
        );

        UPDATE idr
        SET idr.DocRefID = di.KeepDocRefID
        FROM [kb].[IdeaDocRef] idr
        JOIN DupeIds di ON idr.DocRefID = di.DupeDocRefID;

        -- Hard delete duplicates to satisfy the restored UNIQUE constraint
        DELETE dr
        FROM [kb].[DocRef] dr
        JOIN DupeIds di ON dr.DocRefID = di.DupeDocRefID;
        """
    )

    op.create_unique_constraint(
        "UQ_DocRef_DocPath_AnchorID_SnapshotCommitSHA",
        "DocRef",
        ["DocPath", "AnchorID", "SnapshotCommitSHA"],
        schema="kb",
    )

