-- Story 5.6: Manual SQL for Publish Request Workflow
-- Run this if alembic upgrade head did not apply migration 042.
-- Execute against your EventLeadPlatform database.

-- 1. Add RequirePublishApproval to dbo.CompanyFormTestConfig
IF NOT EXISTS (
    SELECT 1 FROM sys.columns c
    INNER JOIN sys.tables t ON c.object_id = t.object_id
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'dbo' AND t.name = 'CompanyFormTestConfig' AND c.name = 'RequirePublishApproval'
)
BEGIN
    ALTER TABLE [dbo].[CompanyFormTestConfig]
    ADD [RequirePublishApproval] BIT NOT NULL DEFAULT 0;
END
GO

-- 2. Add PENDING_REVIEW to ref.FormStatus (if not exists)
IF NOT EXISTS (SELECT 1 FROM [ref].[FormStatus] WHERE StatusCode = N'PENDING_REVIEW')
BEGIN
    INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy)
    VALUES (N'PENDING_REVIEW', N'Pending Admin Review', N'Form requested for publish; awaiting admin review', N'#17A2B8', N'review-icon', 1, 2, 1);
END
GO

-- 3. Create FormPublishRequest table (if not exists)
IF NOT EXISTS (SELECT 1 FROM sys.tables t INNER JOIN sys.schemas s ON t.schema_id = s.schema_id WHERE s.name = 'dbo' AND t.name = 'FormPublishRequest')
BEGIN
    CREATE TABLE [dbo].[FormPublishRequest] (
        [FormPublishRequestID] BIGINT IDENTITY(1,1) NOT NULL,
        [FormID] BIGINT NOT NULL,
        [RequestedBy] BIGINT NOT NULL,
        [RequestedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [Message] NVARCHAR(1000) NULL,
        [Status] NVARCHAR(20) NOT NULL DEFAULT N'pending',
        [CompanyID] BIGINT NOT NULL,
        [CreatedDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        [CreatedBy] BIGINT NULL,
        [UpdatedDate] DATETIME2 NULL,
        [UpdatedBy] BIGINT NULL,
        CONSTRAINT [PK_FormPublishRequest] PRIMARY KEY ([FormPublishRequestID]),
        CONSTRAINT [FK_FormPublishRequest_FormID] FOREIGN KEY ([FormID]) REFERENCES [dbo].[Form]([FormID]),
        CONSTRAINT [FK_FormPublishRequest_RequestedBy] FOREIGN KEY ([RequestedBy]) REFERENCES [dbo].[User]([UserID]),
        CONSTRAINT [FK_FormPublishRequest_CompanyID] FOREIGN KEY ([CompanyID]) REFERENCES [dbo].[Company]([CompanyID]),
        CONSTRAINT [FK_FormPublishRequest_CreatedBy] FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[User]([UserID]),
        CONSTRAINT [FK_FormPublishRequest_UpdatedBy] FOREIGN KEY ([UpdatedBy]) REFERENCES [dbo].[User]([UserID])
    );
    CREATE INDEX [IX_FormPublishRequest_FormID] ON [dbo].[FormPublishRequest]([FormID]);
    CREATE INDEX [IX_FormPublishRequest_CompanyID_Status] ON [dbo].[FormPublishRequest]([CompanyID], [Status]);
    CREATE INDEX [IX_FormPublishRequest_RequestedAt] ON [dbo].[FormPublishRequest]([RequestedAt]);
END
GO

-- 4. Stamp alembic_version to 042 (optional - only if you want alembic to think 042 ran)
-- UPDATE [dbo].[alembic_version] SET version_num = '042' WHERE version_num = '041';
