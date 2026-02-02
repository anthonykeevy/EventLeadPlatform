-- SQL Query to summarize resize.capture events by capture run
-- Groups events by captureRunId and shows key metrics per phase
--
-- Usage:
--   1. Optionally set @ComponentID and @HoursBack to filter
--   2. Run to see summary statistics per resize operation

DECLARE @ComponentID NVARCHAR(100) = NULL;  -- Set to specific component ID, or NULL for all
DECLARE @HoursBack INT = 2;                 -- Look back N hours

WITH CaptureEvents AS (
    SELECT 
        e.FrontendEventID,
        e.CreatedDate,
        e.ComponentID,
        e.ComponentType,
        JSON_VALUE(e.Payload, '$.captureRunId') AS CaptureRunId,
        JSON_VALUE(e.Payload, '$.phase') AS Phase,
        JSON_VALUE(e.Payload, '$.handle') AS Handle,
        CAST(JSON_VALUE(e.Payload, '$.sampleIndex') AS INT) AS SampleIndex,
        CAST(JSON_VALUE(e.Payload, '$.mouse.client.x') AS FLOAT) AS MouseX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.client.y') AS FLOAT) AS MouseY,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.x') AS FLOAT) AS DeltaX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.y') AS FLOAT) AS DeltaY,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.bounds.width') AS FLOAT) AS BoundsWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.bounds.height') AS FLOAT) AS BoundsHeight,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.width') AS FLOAT) AS InputWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.height') AS FLOAT) AS InputHeight,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.isTextWrapped') AS BIT) AS InputIsWrapped
    FROM log.FrontendEvent e
    WHERE e.EventType = 'resize.capture'
        AND (@ComponentID IS NULL OR e.ComponentID = @ComponentID)
        AND e.CreatedDate >= DATEADD(HOUR, -@HoursBack, GETUTCDATE())
),
RunSummary AS (
    SELECT 
        CaptureRunId,
        ComponentID,
        ComponentType,
        Handle,
        MIN(CreatedDate) AS StartTime,
        MAX(CreatedDate) AS EndTime,
        -- Phase counts
        SUM(CASE WHEN Phase = 'start.beforeGrab' THEN 1 ELSE 0 END) AS BeforeGrabCount,
        SUM(CASE WHEN Phase = 'start.afterGrab' THEN 1 ELSE 0 END) AS AfterGrabCount,
        SUM(CASE WHEN Phase = 'sample' THEN 1 ELSE 0 END) AS SampleCount,
        SUM(CASE WHEN Phase = 'beforeDrop' THEN 1 ELSE 0 END) AS BeforeDropCount,
        SUM(CASE WHEN Phase = 'afterDrop' THEN 1 ELSE 0 END) AS AfterDropCount,
        -- Start sizes (from start.afterGrab)
        MAX(CASE WHEN Phase = 'start.afterGrab' THEN BoundsWidth END) AS StartBoundsWidth,
        MAX(CASE WHEN Phase = 'start.afterGrab' THEN BoundsHeight END) AS StartBoundsHeight,
        MAX(CASE WHEN Phase = 'start.afterGrab' THEN InputWidth END) AS StartInputWidth,
        MAX(CASE WHEN Phase = 'start.afterGrab' THEN InputHeight END) AS StartInputHeight,
        -- End sizes (from afterDrop)
        MAX(CASE WHEN Phase = 'afterDrop' THEN BoundsWidth END) AS EndBoundsWidth,
        MAX(CASE WHEN Phase = 'afterDrop' THEN BoundsHeight END) AS EndBoundsHeight,
        MAX(CASE WHEN Phase = 'afterDrop' THEN InputWidth END) AS EndInputWidth,
        MAX(CASE WHEN Phase = 'afterDrop' THEN InputHeight END) AS EndInputHeight,
        -- Mouse movement stats
        MIN(MouseX) AS MinMouseX,
        MAX(MouseX) AS MaxMouseX,
        MIN(MouseY) AS MinMouseY,
        MAX(MouseY) AS MaxMouseY,
        SUM(ABS(DeltaX)) AS TotalDeltaX,
        SUM(ABS(DeltaY)) AS TotalDeltaY,
        -- Wrap events
        SUM(CASE WHEN Phase = 'sample' AND InputIsWrapped = 1 THEN 1 ELSE 0 END) AS WrappedSampleCount
    FROM CaptureEvents
    WHERE CaptureRunId IS NOT NULL
    GROUP BY CaptureRunId, ComponentID, ComponentType, Handle
)
SELECT 
    CaptureRunId,
    ComponentID,
    ComponentType,
    Handle,
    StartTime,
    EndTime,
    DATEDIFF(MILLISECOND, StartTime, EndTime) AS DurationMs,
    -- Phase counts
    BeforeGrabCount,
    AfterGrabCount,
    SampleCount,
    BeforeDropCount,
    AfterDropCount,
    -- Size changes
    StartBoundsWidth,
    EndBoundsWidth,
    EndBoundsWidth - StartBoundsWidth AS DeltaBoundsWidth,
    StartBoundsHeight,
    EndBoundsHeight,
    EndBoundsHeight - StartBoundsHeight AS DeltaBoundsHeight,
    StartInputWidth,
    EndInputWidth,
    EndInputWidth - StartInputWidth AS DeltaInputWidth,
    StartInputHeight,
    EndInputHeight,
    EndInputHeight - StartInputHeight AS DeltaInputHeight,
    -- Mouse movement
    MaxMouseX - MinMouseX AS MouseRangeX,
    MaxMouseY - MinMouseY AS MouseRangeY,
    TotalDeltaX AS TotalMouseDeltaX,
    TotalDeltaY AS TotalMouseDeltaY,
    -- Wrap events
    WrappedSampleCount
FROM RunSummary
ORDER BY StartTime DESC, CaptureRunId;
