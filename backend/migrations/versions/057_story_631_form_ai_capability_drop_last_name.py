"""Story 6.3.1 UAT round 5 (run 42): Drop ``last-name`` from the active
ComponentCapabilitySnapshot until the frontend ``ComponentRegistry`` ships a
matching renderer.

Background — why this rolls back part of migration 056:

UAT run 42 was the first run after migrations 055+056 were applied. Generation
itself succeeded (LLM emitted ``componentType: "last-name"`` and the semantic
gate accepted it), and the compiler laid the form out cleanly with the
``last-name`` tier widths (180 / 260 / 360). But the rendered form on the
canvas was visibly broken — the **Last name field rendered without its label
chrome** because:

  - frontend/src/features/builder/types/builder.types.ts (``ComponentType``
    union) does not list ``'last-name'``.
  - frontend/src/features/builder/registry/ComponentRegistry.tsx has a
    ``'first-name'`` entry but no ``'last-name'`` entry.

Without a registry entry the canvas falls back to a generic input and skips
the label / validation chrome — exactly what the user observed in run 42.

We have two choices to close the gap:

  1. Add ``last-name`` to the frontend ``ComponentType`` union + a matching
     ``ComponentRegistry`` entry + a toolbox preview.
  2. Drop ``last-name`` from the snapshot so the LLM falls back to ``text``
     for last-name fields. The compiler's ``NAME_FIELD_LABELS`` already
     detects "Last name" / "Surname" / "Family name" labels and applies the
     narrow first-name/last-name tier widths even when the type is ``text``,
     so the visual layout stays tight.

We're going with (2) for the short-term Australian-market launch UAT pass —
it unblocks the user's planned 10-prompt bulk test today, and adding a
frontend renderer can land as a focused follow-up story without holding up
the AI workflow refinement.

``first-name`` is left registered because the frontend already supports it
fully (POC component from earlier work).

Revision ID: 057
Revises: 056
Create Date: 2026-04-21
"""

from alembic import op


revision = "057"
down_revision = "056"
branch_labels = None
depends_on = None


# Story 6.3.1 UAT round 5: re-issue the full snapshot WITHOUT ``last-name``.
# Everything else mirrors v3 exactly — only ``last-name`` is removed.
NEW_SNAPSHOT_VERSION = "cf-6.3.1-v4"
NEW_SNAPSHOT_JSON = (
    '{"components":['
    '{"type":"text","widthClasses":["compact","half","full"]},'
    '{"type":"first-name","widthClasses":["half","full"]},'
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
                -- not by content hash.
                N'uat-round5-drop-last-name-no-frontend-renderer',
                0,
                @Now,
                @Now,
                0
            );
        END

        -- Single-active-row invariant: deactivate every other snapshot, then
        -- activate v4.
        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
          AND [IsDeleted] = 0;
        """
    )

    # We deliberately leave the ``last-name`` ``ComponentValidationContract``
    # row in place (added by 056). It is harmless — the semantic validator
    # only consults contracts for types that ARE in the active snapshot, and
    # leaving it means re-adding ``last-name`` later is just a snapshot bump
    # rather than another contract migration.


def downgrade() -> None:
    bind = op.get_bind()

    # Reactivate v3 (which had last-name).
    bind.exec_driver_sql(
        f"""
        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [SnapshotVersion] = N'{NEW_SNAPSHOT_VERSION}'
          AND [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'cf-6.3.1-v3'
          AND [IsDeleted] = 0;
        """
    )
