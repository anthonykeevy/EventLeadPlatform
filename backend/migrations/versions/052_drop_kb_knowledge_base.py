"""Remove SQL KB schema (kb) — Kaizen / agent-tools KB retired

Revision ID: 052
Revises: 051
Create Date: 2026-03-31

Purpose:
- Drop schema [kb] and all objects created by revisions 036–037.
- Historical migrations 036/037 remain in the tree for Alembic ancestry; this revision
  removes live database objects on upgraded environments.

Note: downgrade is not supported (data and DDL are not restored).
"""

from alembic import op


revision = "052"
down_revision = "051"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # DocRef filtered unique indexes from 037 (no-op if already absent)
    op.execute(
        """
        IF OBJECT_ID(N'kb.DocRef', N'U') IS NOT NULL
        BEGIN
            IF EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID(N'kb.DocRef') AND name = N'IX_DocRef_Unique_DocPath_A0_S0')
                DROP INDEX [IX_DocRef_Unique_DocPath_A0_S0] ON [kb].[DocRef];
            IF EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID(N'kb.DocRef') AND name = N'IX_DocRef_Unique_DocPath_AnchorID_S0')
                DROP INDEX [IX_DocRef_Unique_DocPath_AnchorID_S0] ON [kb].[DocRef];
            IF EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID(N'kb.DocRef') AND name = N'IX_DocRef_Unique_DocPath_A0_SnapshotCommitSHA')
                DROP INDEX [IX_DocRef_Unique_DocPath_A0_SnapshotCommitSHA] ON [kb].[DocRef];
            IF EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID(N'kb.DocRef') AND name = N'IX_DocRef_Unique_DocPath_AnchorID_SnapshotCommitSHA')
                DROP INDEX [IX_DocRef_Unique_DocPath_AnchorID_SnapshotCommitSHA] ON [kb].[DocRef];
        END
        """
    )

    op.execute(
        """
        IF OBJECT_ID(N'kb.DocRef', N'U') IS NOT NULL
           AND EXISTS (
               SELECT 1 FROM sys.key_constraints
               WHERE parent_object_id = OBJECT_ID(N'kb.DocRef')
                 AND name = N'UQ_DocRef_DocPath_AnchorID_SnapshotCommitSHA'
           )
            ALTER TABLE [kb].[DocRef] DROP CONSTRAINT [UQ_DocRef_DocPath_AnchorID_SnapshotCommitSHA];
        """
    )

    op.execute(
        """
        IF OBJECT_ID(N'[kb].[TR_Idea_SetUpdatedDate]', N'TR') IS NOT NULL
            DROP TRIGGER [kb].[TR_Idea_SetUpdatedDate];
        """
    )
    op.execute(
        """
        IF OBJECT_ID(N'[kb].[TR_Aspect_SetUpdatedDate]', N'TR') IS NOT NULL
            DROP TRIGGER [kb].[TR_Aspect_SetUpdatedDate];
        """
    )

    op.execute(
        """
        IF OBJECT_ID(N'[kb].[EnqueueRelatedAspectReviews]', N'P') IS NOT NULL
            DROP PROCEDURE [kb].[EnqueueRelatedAspectReviews];
        """
    )

    op.execute(
        """
        IF OBJECT_ID(N'kb.ReviewTask', N'U') IS NOT NULL DROP TABLE [kb].[ReviewTask];
        IF OBJECT_ID(N'kb.IdeaDocRef', N'U') IS NOT NULL DROP TABLE [kb].[IdeaDocRef];
        IF OBJECT_ID(N'kb.AspectDocRef', N'U') IS NOT NULL DROP TABLE [kb].[AspectDocRef];
        IF OBJECT_ID(N'kb.DocRef', N'U') IS NOT NULL DROP TABLE [kb].[DocRef];

        IF OBJECT_ID(N'kb.SessionNoteAspect', N'U') IS NOT NULL DROP TABLE [kb].[SessionNoteAspect];
        IF OBJECT_ID(N'kb.SessionNoteIdea', N'U') IS NOT NULL DROP TABLE [kb].[SessionNoteIdea];
        IF OBJECT_ID(N'kb.SessionNote', N'U') IS NOT NULL DROP TABLE [kb].[SessionNote];

        IF OBJECT_ID(N'kb.AspectWorkItem', N'U') IS NOT NULL DROP TABLE [kb].[AspectWorkItem];
        IF OBJECT_ID(N'kb.IdeaWorkItem', N'U') IS NOT NULL DROP TABLE [kb].[IdeaWorkItem];
        IF OBJECT_ID(N'kb.WorkItem', N'U') IS NOT NULL DROP TABLE [kb].[WorkItem];

        IF OBJECT_ID(N'kb.IdeaAspect', N'U') IS NOT NULL DROP TABLE [kb].[IdeaAspect];
        IF OBJECT_ID(N'kb.AspectRelation', N'U') IS NOT NULL DROP TABLE [kb].[AspectRelation];
        IF OBJECT_ID(N'kb.Idea', N'U') IS NOT NULL DROP TABLE [kb].[Idea];
        IF OBJECT_ID(N'kb.Aspect', N'U') IS NOT NULL DROP TABLE [kb].[Aspect];

        IF OBJECT_ID(N'kb.ReviewTaskStatus', N'U') IS NOT NULL DROP TABLE [kb].[ReviewTaskStatus];
        IF OBJECT_ID(N'kb.WorkItemType', N'U') IS NOT NULL DROP TABLE [kb].[WorkItemType];
        IF OBJECT_ID(N'kb.RelationType', N'U') IS NOT NULL DROP TABLE [kb].[RelationType];
        IF OBJECT_ID(N'kb.IdeaStatus', N'U') IS NOT NULL DROP TABLE [kb].[IdeaStatus];
        IF OBJECT_ID(N'kb.AspectState', N'U') IS NOT NULL DROP TABLE [kb].[AspectState];
        IF OBJECT_ID(N'kb.MaturityLevel', N'U') IS NOT NULL DROP TABLE [kb].[MaturityLevel];
        """
    )

    op.execute(
        """
        IF EXISTS (SELECT * FROM sys.schemas WHERE name = N'kb')
            EXEC(N'DROP SCHEMA [kb]');
        """
    )


def downgrade() -> None:
    raise NotImplementedError("052 removes KB schema; restore from backup or re-apply revisions 036–037 manually if needed.")
