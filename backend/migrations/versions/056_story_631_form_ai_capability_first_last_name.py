"""Story 6.3.1 UAT round 5 (run 41): Extend ComponentCapabilitySnapshot with
``first-name`` and ``last-name`` so the LLM can pick the right semantic component
type instead of having the semantic gate reject it as ``unknown-component-type``.

Background — why this migration exists:

UAT run 41 took 3 attempts (validated-success but inefficient). Attempt 2 of 3
was wasted on this exact gate failure:

    {"code":"unknown-component-type","componentType":"first-name", ... }

The compiler already has tier widths for ``first-name`` / ``last-name`` (see
``COMPONENT_WIDTH_TIERS`` in ``modules/form_ai/compiler.py`` lines 51-52) and
the frontend renderer already supports them — the only missing piece was the
governance row that tells the semantic gate they're allowed. Adding them here
lets the LLM emit the type it naturally wants on attempt 1 and saves a full
correction round trip.

Width classes mirror ``text`` minus ``compact`` (a 180 px name field is already
on the small end of comfortable; allowing ``compact`` would just push it below
the 160 px content readability threshold).

Revision ID: 056
Revises: 055
Create Date: 2026-04-21
"""

from alembic import op


revision = "056"
down_revision = "055"
branch_labels = None
depends_on = None


# Story 6.3.1 UAT round 5: a new snapshot version is the cleanest way to roll
# the additions forward (the existing v2 from migration 055 is left intact and
# simply deactivated). Adds:
#   - first-name   (widthClasses: half, full)
#   - last-name    (widthClasses: half, full)
#
# Everything else mirrors v2 (rating, file-upload, address, url already added
# there) so the LLM still has access to the full palette.
NEW_SNAPSHOT_VERSION = "cf-6.3.1-v3"
NEW_SNAPSHOT_JSON = (
    '{"components":['
    '{"type":"text","widthClasses":["compact","half","full"]},'
    '{"type":"first-name","widthClasses":["half","full"]},'
    '{"type":"last-name","widthClasses":["half","full"]},'
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

    # 1. Insert the v3 snapshot row if it doesn't already exist, then activate
    #    it (deactivating every other snapshot in the process — there is only
    #    ever one active snapshot per the existing service contract).
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
                N'uat-round5-first-last-name',
                0,
                @Now,
                @Now,
                0
            );
        END

        -- Single-active-row invariant: deactivate every other snapshot, then
        -- activate the v3 row.
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
    #    NOT EXISTS guards a re-run from inserting duplicates).
    #
    #    first-name / last-name use the same rule shape as ``text`` — required
    #    + length bounds. No format/pattern rule because there is no canonical
    #    regex for personal names (Unicode, hyphens, apostrophes, single-char
    #    initials all need to pass).
    bind.exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        ;WITH ContractRows AS (
            SELECT *
            FROM (VALUES
                (N'first-name', N'v1', N'["required","minLength","maxLength","pattern"]'),
                (N'last-name',  N'v1', N'["required","minLength","maxLength","pattern"]')
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
            N'{"required":{"type":"boolean"},"minLength":{"type":"integer","minimum":0},"maxLength":{"type":"integer","minimum":1},"pattern":{"type":"string"}}',
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

    # Reactivate the previous snapshot (v2 from migration 055) and deactivate
    # v3. We don't try to walk further back — if 055 was never applied,
    # reactivating v1 is the next downgrade's job (055.downgrade()).
    bind.exec_driver_sql(
        f"""
        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
          AND [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'cf-6.3.1-v2'
          AND [IsDeleted] = 0;
        """
    )

    # Leave the validation contract rows in place. They are additive metadata
    # and removing them risks breaking other tooling that reads the contract
    # table independently.
