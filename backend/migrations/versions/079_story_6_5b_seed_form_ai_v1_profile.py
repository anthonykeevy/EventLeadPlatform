"""Story 6.5b: Seed FORM_AI_V1 PromptAssemblyRegistry + version + 5 sections.

Revision ID: 079
Revises: 078
Create Date: 2026-05-20

Seeds the foundational registry rows for Story 6.5b:
  * 1 PromptAssemblyRegistry row: Code='FORM_AI_V1'
  * 1 PromptAssemblyRegistryVersion row: VersionNumber=1, IsActive=1
  * 5 PromptSection rows: A=ROLE_CONTRACT, B=SAFETY, C=BRAND_POSTURE, G=FEW_SHOT, I=JSON_OUTPUT

SortOrder values reflect the *current emission order* of the in-scope blocks
inside backend/modules/form_ai/service.py::_build_initial_messages
(A=10, B=20, I=30, G=40, C=50). This deviates from the architectural
A-then-B-then-C-then-...-then-I sort order documented in
prompt-assembly-registry-architecture.md so that AC-19 can land at
"Identical" byte-equivalence for unchanged inputs. SortOrder will be
reconciled to A->I order in Story 6.5c when Block F (capability) and
Block D (locale) are migrated into the registry and the renderer
becomes the authoritative orchestrator (rather than hand-glued by
_build_initial_messages).

Variants are seeded in subsequent migrations (080 = A/B/C/I, 081 = G).
"""

from alembic import op


revision = "079"
down_revision = "078"
branch_labels = None
depends_on = None


REGISTRY_CODE = "FORM_AI_V1"


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        ------------------------------------------------------------------
        -- 1. PromptAssemblyRegistry row
        ------------------------------------------------------------------
        DECLARE @RegistryID BIGINT;
        SELECT @RegistryID = [PromptAssemblyRegistryID]
        FROM [config].[PromptAssemblyRegistry]
        WHERE [Code] = N'FORM_AI_V1' AND [IsDeleted] = 0;

        IF @RegistryID IS NULL
        BEGIN
            INSERT INTO [config].[PromptAssemblyRegistry]
                ([Code], [Description], [IsActive], [CreatedUtc], [IsDeleted])
            VALUES
            (
                N'FORM_AI_V1',
                N'Form AI generation prompt assembly - initial migration of stored prose blocks (A/B/C/G/I).',
                1,
                @Now,
                0
            );
            SET @RegistryID = SCOPE_IDENTITY();
        END

        ------------------------------------------------------------------
        -- 2. PromptAssemblyRegistryVersion row (VersionNumber=1, IsActive=1)
        ------------------------------------------------------------------
        DECLARE @VersionID BIGINT;
        SELECT @VersionID = [PromptAssemblyRegistryVersionID]
        FROM [config].[PromptAssemblyRegistryVersion]
        WHERE [PromptAssemblyRegistryID] = @RegistryID
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        IF @VersionID IS NULL
        BEGIN
            INSERT INTO [config].[PromptAssemblyRegistryVersion]
            (
                [PromptAssemblyRegistryID],
                [VersionNumber],
                [IsActive],
                [IsLockedForEdits],
                [ReleaseNotes],
                [ActivatedUtc],
                [CreatedUtc],
                [IsDeleted]
            )
            VALUES
            (
                @RegistryID,
                1,
                1,
                0,
                N'Initial registry - A/B/C/G/I migration; D/E/F/H remain on existing paths in Story 6.5b. Reconciled to A->I order in 6.5c.',
                @Now,
                @Now,
                0
            );
            SET @VersionID = SCOPE_IDENTITY();
        END

        ------------------------------------------------------------------
        -- 3. PromptSection rows (5 rows: A, B, I, G, C in emission order)
        --    SortOrder reflects current _build_initial_messages emission
        --    order (NOT architectural A->I order; reconciled in 6.5c).
        ------------------------------------------------------------------
        ;WITH SectionRows AS (
            SELECT *
            FROM (VALUES
                (N'A', N'ROLE_CONTRACT',  10, N'Prose'),
                (N'B', N'SAFETY',         20, N'Prose'),
                (N'I', N'JSON_OUTPUT',    30, N'Prose'),
                (N'G', N'FEW_SHOT',       40, N'Prose'),
                (N'C', N'BRAND_POSTURE',  50, N'Prose')
            ) AS rows ([SectionCode], [DisplayName], [SortOrder], [DataStructureType])
        )
        INSERT INTO [config].[PromptSection]
        (
            [PromptAssemblyRegistryVersionID],
            [SectionCode],
            [DisplayName],
            [SortOrder],
            [IsRequired],
            [DataStructureType],
            [Heading],
            [CreatedUtc],
            [IsDeleted]
        )
        SELECT
            @VersionID,
            r.[SectionCode],
            r.[DisplayName],
            r.[SortOrder],
            1,
            r.[DataStructureType],
            NULL,
            @Now,
            0
        FROM SectionRows r
        WHERE NOT EXISTS (
            SELECT 1
            FROM [config].[PromptSection] existing
            WHERE existing.[PromptAssemblyRegistryVersionID] = @VersionID
              AND existing.[SectionCode] = r.[SectionCode]
              AND existing.[IsDeleted] = 0
        );
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @RegistryID BIGINT = (
            SELECT TOP 1 [PromptAssemblyRegistryID]
            FROM [config].[PromptAssemblyRegistry]
            WHERE [Code] = N'FORM_AI_V1' AND [IsDeleted] = 0
        );

        IF @RegistryID IS NULL RETURN;

        DECLARE @VersionID BIGINT = (
            SELECT TOP 1 [PromptAssemblyRegistryVersionID]
            FROM [config].[PromptAssemblyRegistryVersion]
            WHERE [PromptAssemblyRegistryID] = @RegistryID
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        );

        IF @VersionID IS NULL
        BEGIN
            DELETE FROM [config].[PromptAssemblyRegistry] WHERE [PromptAssemblyRegistryID] = @RegistryID;
            RETURN;
        END

        -- Hard-delete sections seeded by this migration (variants seeded by
        -- 080/081 will already be gone by the time this downgrade runs).
        DELETE FROM [config].[PromptSection]
        WHERE [PromptAssemblyRegistryVersionID] = @VersionID
          AND [SectionCode] IN (N'A', N'B', N'C', N'G', N'I');

        DELETE FROM [config].[PromptAssemblyRegistryVersion]
        WHERE [PromptAssemblyRegistryVersionID] = @VersionID;

        DELETE FROM [config].[PromptAssemblyRegistry]
        WHERE [PromptAssemblyRegistryID] = @RegistryID;
        """
    )
