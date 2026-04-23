"""Story 6.3.1: Seed baseline Form AI governance versions.

Revision ID: 054
Revises: 053
Create Date: 2026-04-16
"""

from alembic import op


revision = "054"
down_revision = "053"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Seed baseline prompt/capability/snapshot/width-policy rows and one
    # prompt-assembly profile so runtime governance resolution returns active IDs.
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        ------------------------------------------------------------------------
        -- PromptTemplate + PromptTemplateVersion
        ------------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1
            FROM [config].[PromptTemplate]
            WHERE [TemplateKey] = N'FORM_AI_STEP1_BASE'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[PromptTemplate]
            (
                [TemplateKey],
                [TemplateName],
                [Purpose],
                [Owner],
                [IsActive],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                N'FORM_AI_STEP1_BASE',
                N'Form AI Step 1 Semantic Authoring Baseline',
                N'Story 6.3.1 baseline template for simplified semantic output contract.',
                N'form-ai',
                1,
                @Now,
                0
            );
        END

        DECLARE @PromptTemplateID BIGINT =
        (
            SELECT TOP 1 [PromptTemplateID]
            FROM [config].[PromptTemplate]
            WHERE [TemplateKey] = N'FORM_AI_STEP1_BASE'
              AND [IsDeleted] = 0
            ORDER BY [PromptTemplateID] DESC
        );

        IF NOT EXISTS (
            SELECT 1
            FROM [config].[PromptTemplateVersion]
            WHERE [PromptTemplateID] = @PromptTemplateID
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[PromptTemplateVersion]
            (
                [PromptTemplateID],
                [VersionNumber],
                [VersionLabel],
                [TemplateBody],
                [ChangeSummary],
                [ContentHash],
                [IsActive],
                [ActivatedDate],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                @PromptTemplateID,
                1,
                N'6.3.1-baseline',
                N'Step 1 semantic output only: fields, labels, required, options, grouping hints, width intent compact/half/full. No pixel coordinates. Grid-only downstream compile.',
                N'Initial Story 6.3.1 baseline prompt template.',
                N'a90bd6f44a7aa083f3eaf53b3bd2d14d879ebb91ad798ec42cbf84a581be6f6f',
                1,
                @Now,
                @Now,
                0
            );
        END

        UPDATE [config].[PromptTemplateVersion]
        SET [IsActive] = 0
        WHERE [PromptTemplateID] = @PromptTemplateID
          AND [IsDeleted] = 0;

        UPDATE [config].[PromptTemplateVersion]
        SET [IsActive] = 1,
            [ActivatedDate] = COALESCE([ActivatedDate], @Now)
        WHERE [PromptTemplateID] = @PromptTemplateID
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        ------------------------------------------------------------------------
        -- CapabilityPolicyVersion baseline
        ------------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1
            FROM [config].[CapabilityPolicyVersion]
            WHERE [PolicyKey] = N'FORM_AI_CAPABILITY_POLICY'
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[CapabilityPolicyVersion]
            (
                [PolicyKey],
                [VersionNumber],
                [PolicyJson],
                [PolicyHash],
                [IsActive],
                [ActivatedDate],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                N'FORM_AI_CAPABILITY_POLICY',
                1,
                N'{"step1":{"allowSemanticOnly":true,"allowGeometry":false},"step2":{"gridOnly":true,"allowNonGrid":false},"features":{"widthClasses":["compact","half","full"],"validationContractRequired":true}}',
                N'1809340657b84a4a637f48f8ac8afca84cdf74f8f37f721f5bf4b746f9dc2db3',
                1,
                @Now,
                @Now,
                0
            );
        END

        UPDATE [config].[CapabilityPolicyVersion]
        SET [IsActive] = 0
        WHERE [PolicyKey] = N'FORM_AI_CAPABILITY_POLICY'
          AND [IsDeleted] = 0;

        UPDATE [config].[CapabilityPolicyVersion]
        SET [IsActive] = 1,
            [ActivatedDate] = COALESCE([ActivatedDate], @Now)
        WHERE [PolicyKey] = N'FORM_AI_CAPABILITY_POLICY'
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        ------------------------------------------------------------------------
        -- WidthClassPolicyVersion baseline
        ------------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1
            FROM [config].[WidthClassPolicyVersion]
            WHERE [PolicyKey] = N'FORM_AI_WIDTH_POLICY'
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[WidthClassPolicyVersion]
            (
                [PolicyKey],
                [VersionNumber],
                [PolicyJson],
                [PolicyHash],
                [IsActive],
                [ActivatedDate],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                N'FORM_AI_WIDTH_POLICY',
                1,
                N'{"classes":{"compact":{"minSpan":3,"targetSpan":4,"maxSpan":5},"half":{"minSpan":5,"targetSpan":6,"maxSpan":7},"full":{"minSpan":10,"targetSpan":12,"maxSpan":12}},"downgradeRules":[{"if":"canvasWidth<1200","from":"half","to":"full"}]}',
                N'4ab0a19e811746860af290a45401fbe9f008ec3f11a8883aab03d92483399f5f',
                1,
                @Now,
                @Now,
                0
            );
        END

        UPDATE [config].[WidthClassPolicyVersion]
        SET [IsActive] = 0
        WHERE [PolicyKey] = N'FORM_AI_WIDTH_POLICY'
          AND [IsDeleted] = 0;

        UPDATE [config].[WidthClassPolicyVersion]
        SET [IsActive] = 1,
            [ActivatedDate] = COALESCE([ActivatedDate], @Now)
        WHERE [PolicyKey] = N'FORM_AI_WIDTH_POLICY'
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        ------------------------------------------------------------------------
        -- ComponentCapabilitySnapshot baseline
        ------------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1
            FROM [config].[ComponentCapabilitySnapshot]
            WHERE [SnapshotVersion] = N'cf-6.3.1-v1'
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
                N'cf-6.3.1-v1',
                N'{"components":[{"type":"text","widthClasses":["compact","half","full"]},{"type":"email","widthClasses":["compact","half","full"]},{"type":"phone","widthClasses":["compact","half","full"]},{"type":"number","widthClasses":["compact","half","full"]},{"type":"date","widthClasses":["compact","half","full"]},{"type":"textarea","widthClasses":["half","full"]},{"type":"dropdown","widthClasses":["compact","half","full"]},{"type":"checkbox","widthClasses":["half","full"]},{"type":"radio","widthClasses":["half","full"]},{"type":"terms","widthClasses":["full"]},{"type":"submit-button","widthClasses":["compact","half"]},{"type":"header","widthClasses":["full"]},{"type":"paragraph","widthClasses":["full"]},{"type":"divider","widthClasses":["full"]}]}',
                N'7ad7c428f1478ca9b31a5da9fd08aa16d077171d4bf71d2f69dac3b649ef9f88',
                1,
                @Now,
                @Now,
                0
            );
        END

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 1
        WHERE [SnapshotVersion] = N'cf-6.3.1-v1'
          AND [IsDeleted] = 0;

        ------------------------------------------------------------------------
        -- ComponentValidationContract baseline (v1)
        ------------------------------------------------------------------------
        ;WITH ContractRows AS (
            SELECT *
            FROM (VALUES
                (N'text', N'v1', N'["required","minLength","maxLength","pattern"]'),
                (N'email', N'v1', N'["required","email","maxLength"]'),
                (N'phone', N'v1', N'["required","phone","pattern"]'),
                (N'number', N'v1', N'["required","min","max"]'),
                (N'date', N'v1', N'["required"]'),
                (N'address', N'v1', N'["required","maxLength"]'),
                (N'textarea', N'v1', N'["required","minLength","maxLength"]'),
                (N'dropdown', N'v1', N'["required"]'),
                (N'select', N'v1', N'["required"]'),
                (N'checkbox', N'v1', N'["required"]'),
                (N'radio', N'v1', N'["required"]'),
                (N'terms', N'v1', N'["required"]'),
                (N'submit-button', N'v1', N'[]'),
                (N'header', N'v1', N'[]'),
                (N'paragraph', N'v1', N'[]'),
                (N'divider', N'v1', N'[]')
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
            N'{"required":{"type":"boolean"},"minLength":{"type":"integer","minimum":0},"maxLength":{"type":"integer","minimum":1},"min":{"type":"number"},"max":{"type":"number"},"pattern":{"type":"string"}}',
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

        ------------------------------------------------------------------------
        -- PromptAssemblyProfile baseline
        ------------------------------------------------------------------------
        DECLARE @PromptTemplateVersionID BIGINT =
        (
            SELECT TOP 1 [PromptTemplateVersionID]
            FROM [config].[PromptTemplateVersion]
            WHERE [PromptTemplateID] = @PromptTemplateID
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
            ORDER BY [PromptTemplateVersionID] DESC
        );

        DECLARE @CapabilityPolicyVersionID BIGINT =
        (
            SELECT TOP 1 [CapabilityPolicyVersionID]
            FROM [config].[CapabilityPolicyVersion]
            WHERE [PolicyKey] = N'FORM_AI_CAPABILITY_POLICY'
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        );

        DECLARE @WidthClassPolicyVersionID BIGINT =
        (
            SELECT TOP 1 [WidthClassPolicyVersionID]
            FROM [config].[WidthClassPolicyVersion]
            WHERE [PolicyKey] = N'FORM_AI_WIDTH_POLICY'
              AND [VersionNumber] = 1
              AND [IsDeleted] = 0
        );

        IF NOT EXISTS (
            SELECT 1
            FROM [config].[PromptAssemblyProfile]
            WHERE [ProfileKey] = N'FORM_AI_DEFAULT_STEP1'
              AND [StepName] = N'step1'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[PromptAssemblyProfile]
            (
                [ProfileKey],
                [ProfileName],
                [StepName],
                [Description],
                [PromptTemplateVersionID],
                [CapabilityPolicyVersionID],
                [WidthClassPolicyVersionID],
                [IsActive],
                [CreatedDate],
                [IsDeleted]
            )
            VALUES
            (
                N'FORM_AI_DEFAULT_STEP1',
                N'Form AI Default Step 1 Profile',
                N'step1',
                N'Baseline runtime profile for Story 6.3.1 semantic generation.',
                @PromptTemplateVersionID,
                @CapabilityPolicyVersionID,
                @WidthClassPolicyVersionID,
                1,
                @Now,
                0
            );
        END
        ELSE
        BEGIN
            UPDATE [config].[PromptAssemblyProfile]
            SET
                [PromptTemplateVersionID] = @PromptTemplateVersionID,
                [CapabilityPolicyVersionID] = @CapabilityPolicyVersionID,
                [WidthClassPolicyVersionID] = @WidthClassPolicyVersionID,
                [IsActive] = 1,
                [UpdatedDate] = @Now,
                [IsDeleted] = 0
            WHERE [ProfileKey] = N'FORM_AI_DEFAULT_STEP1'
              AND [StepName] = N'step1';
        END
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        UPDATE [config].[PromptAssemblyProfile]
        SET [IsActive] = 0
        WHERE [ProfileKey] = N'FORM_AI_DEFAULT_STEP1'
          AND [StepName] = N'step1'
          AND [IsDeleted] = 0;

        UPDATE [config].[PromptTemplateVersion]
        SET [IsActive] = 0
        WHERE [PromptTemplateID] IN (
            SELECT [PromptTemplateID]
            FROM [config].[PromptTemplate]
            WHERE [TemplateKey] = N'FORM_AI_STEP1_BASE'
              AND [IsDeleted] = 0
        )
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        UPDATE [config].[CapabilityPolicyVersion]
        SET [IsActive] = 0
        WHERE [PolicyKey] = N'FORM_AI_CAPABILITY_POLICY'
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        UPDATE [config].[WidthClassPolicyVersion]
        SET [IsActive] = 0
        WHERE [PolicyKey] = N'FORM_AI_WIDTH_POLICY'
          AND [VersionNumber] = 1
          AND [IsDeleted] = 0;

        UPDATE [config].[ComponentCapabilitySnapshot]
        SET [IsActive] = 0
        WHERE [SnapshotVersion] = N'cf-6.3.1-v1'
          AND [IsDeleted] = 0;
        """
    )
