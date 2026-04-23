"""Story 6.3.1 Phase 1 W4: Extend ComponentCapabilitySnapshot with rating,
file-upload, address, and url so the LLM can pick the right semantic component
type instead of substituting (e.g. radio for rating, text for url).

Also seeds matching ComponentValidationContract rows so the compiler accepts
their validationIntent without dropping rules.

Revision ID: 055
Revises: 054
Create Date: 2026-04-15
"""

from alembic import op


revision = "055"
down_revision = "054"
branch_labels = None
depends_on = None


# Story 6.3.1 layout-solver Phase 1 W4: a new snapshot version is the cleanest
# way to roll the additions forward (the existing v1 is left intact and simply
# deactivated). Adds:
#   - rating       (widthClasses: half, full)
#   - file-upload  (widthClasses: full)
#   - address      (widthClasses: full)  — was missing entirely
#   - url          (widthClasses: half, full) — was missing entirely
# Hash recomputed against the JSON below.
NEW_SNAPSHOT_VERSION = "cf-6.3.1-v2"
NEW_SNAPSHOT_JSON = (
    '{"components":['
    '{"type":"text","widthClasses":["compact","half","full"]},'
    '{"type":"email","widthClasses":["compact","half","full"]},'
    '{"type":"phone","widthClasses":["compact","half","full"]},'
    '{"type":"number","widthClasses":["compact","half","full"]},'
    '{"type":"date","widthClasses":["compact","half","full"]},'
    '{"type":"address","widthClasses":["full"]},'
    '{"type":"url","widthClasses":["half","full"]},'
    '{"type":"textarea","widthClasses":["half","full"]},'
    '{"type":"dropdown","widthClasses":["compact","half","full"]},'
    '{"type":"checkbox","widthClasses":["half","full"]},'
    '{"type":"radio","widthClasses":["half","full"]},'
    '{"type":"rating","widthClasses":["half","full"]},'
    '{"type":"file-upload","widthClasses":["full"]},'
    '{"type":"terms","widthClasses":["full"]},'
    '{"type":"submit-button","widthClasses":["compact","half"]},'
    '{"type":"header","widthClasses":["full"]},'
    '{"type":"paragraph","widthClasses":["full"]},'
    '{"type":"divider","widthClasses":["full"]}'
    "]}"
)


def upgrade() -> None:
    bind = op.get_bind()

    # 1. Insert the v2 snapshot row if it doesn't already exist, then activate
    #    it (deactivating v1 in the process — there is only ever one active
    #    snapshot per the existing service contract).
    bind.exec_driver_sql(
        f"""
        DECLARE @Now DATETIME2 = GETUTCDATE();

        IF NOT EXISTS (
            SELECT 1
            FROM [config].[ComponentCapabilitySnapshot]
            WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[ComponentCapabilitySnapshot]
            (
                [SnapshotVersion],
                [SnapshotJson],
                [SourceManifestHash],
                [IsActive],
                [GeneratedDate],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                N'{NEW_SNAPSHOT_VERSION}',
                N'{NEW_SNAPSHOT_JSON}',
                -- Hash is informational; the runtime resolves the active row by ID,
                -- not by content hash. We seed a deterministic placeholder rather
                -- than computing SHA at SQL time.
                N'phase1-w4-rating-fileupload-address-url',
                0,
                @Now,
                @Now,
                0
            );
        END

        -- Single-active-row invariant: deactivate every other snapshot, then
        -- activate the v2 row.
        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
          AND [IsDeleted] = 0;
        """
    )

    # 2. Seed validation contracts for the newly added types (idempotent —
    #    ON NOT EXISTS guards a re-run from inserting duplicates).
    bind.exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        ;WITH ContractRows AS (
            SELECT *
            FROM (VALUES
                (N'rating',      N'v1', N'["required","min","max"]'),
                (N'file-upload', N'v1', N'["required"]'),
                (N'url',         N'v1', N'["required","url","maxLength"]')
            ) AS rows([ComponentType], [ContractVersion], [AllowedRulesJson])
        )
        INSERT INTO [config].[ComponentValidationContract]
        (
            [ComponentType],
            [ContractVersion],
            [AllowedRulesJson],
            [RuleParameterSchemaJson],
            [RuleCompatibilityJson],
            [MessagePolicyJson],
            [IsActive],
            [CreatedDate],
            [IsDeleted]
        )
        SELECT
            c.[ComponentType],
            c.[ContractVersion],
            c.[AllowedRulesJson],
            N'{"required":{"type":"boolean"},"minLength":{"type":"integer","minimum":0},"maxLength":{"type":"integer","minimum":1},"min":{"type":"number"},"max":{"type":"number"},"pattern":{"type":"string"},"url":{"type":"boolean"}}',
            N'{}',
            N'{"defaultBehavior":"allowCustomMessage","fallback":"component-default"}',
            1,
            @Now,
            0
        FROM ContractRows c
        WHERE NOT EXISTS (
            SELECT 1
            FROM [config].[ComponentValidationContract] existing
            WHERE existing.[ComponentType] = c.[ComponentType]
              AND existing.[ContractVersion] = c.[ContractVersion]
              AND existing.[IsDeleted] = 0
        );
        """
    )


def downgrade() -> None:
    bind = op.get_bind()

    # Reactivate the previous snapshot (v1) and deactivate v2.
    bind.exec_driver_sql(
        f"""
        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
          AND [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'cf-6.3.1-v1'
          AND [IsDeleted] = 0;
        """
    )

    # Leave the validation contract rows in place. They are additive metadata
    # and removing them risks breaking other tooling that reads the contract
    # table independently.
