-- SQL Query to view resize.capture events in table format
-- Extracts key fields from JSON payload for easy analysis
--
-- Usage:
--   1. Optionally set @ComponentID and @HoursBack to filter
--   2. Run the query to see all resize capture events
--
-- Adjust TOP value if you need more/fewer rows

DECLARE @ComponentID NVARCHAR(100) = NULL;  -- Set to specific component ID, or NULL for all
DECLARE @HoursBack INT = 2;                 -- Look back N hours

SELECT TOP 500
    e.FrontendEventID,
    e.CreatedDate,
    e.ComponentID,
    e.ComponentType,
    e.SessionID,
    
    -- Capture metadata
    JSON_VALUE(e.Payload, '$.captureRunId') AS CaptureRunId,
    JSON_VALUE(e.Payload, '$.phase') AS Phase,
    JSON_VALUE(e.Payload, '$.handle') AS Handle,
    JSON_VALUE(e.Payload, '$.sampleIndex') AS SampleIndex,
    JSON_VALUE(e.Payload, '$.reason') AS Reason,
    
    -- Mouse position and deltas
    JSON_VALUE(e.Payload, '$.mouse.client.x') AS MouseClientX,
    JSON_VALUE(e.Payload, '$.mouse.client.y') AS MouseClientY,
    JSON_VALUE(e.Payload, '$.mouse.start.x') AS MouseStartX,
    JSON_VALUE(e.Payload, '$.mouse.start.y') AS MouseStartY,
    JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.x') AS DeltaFromPrevX,
    JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.y') AS DeltaFromPrevY,
    JSON_VALUE(e.Payload, '$.mouse.deltaFromStart.x') AS DeltaFromStartX,
    JSON_VALUE(e.Payload, '$.mouse.deltaFromStart.y') AS DeltaFromStartY,
    JSON_VALUE(e.Payload, '$.mouse.ts') AS MouseTimestamp,
    
    -- Component bounds (from snapshot)
    JSON_VALUE(e.Payload, '$.snapshot.bounds.width') AS BoundsWidth,
    JSON_VALUE(e.Payload, '$.snapshot.bounds.height') AS BoundsHeight,
    JSON_VALUE(e.Payload, '$.snapshot.bounds.left') AS BoundsLeft,
    JSON_VALUE(e.Payload, '$.snapshot.bounds.top') AS BoundsTop,
    
    -- SmartBorder bounds
    JSON_VALUE(e.Payload, '$.snapshot.smartBorderBounds.width') AS SmartBorderWidth,
    JSON_VALUE(e.Payload, '$.snapshot.smartBorderBounds.height') AS SmartBorderHeight,
    
    -- Input object metrics (if present)
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.width') AS InputWidth,
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.height') AS InputHeight,
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.isTextWrapped') AS InputIsWrapped,
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.scrollWidth') AS InputScrollWidth,
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.clientWidth') AS InputClientWidth,
    JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.lineCount') AS InputLineCount,
    
    -- SmartBorder geometry (from geometry object)
    JSON_VALUE(e.Payload, '$.geometry.smartBorder.bbox.width') AS SmartBorderBboxWidth,
    JSON_VALUE(e.Payload, '$.geometry.smartBorder.bbox.height') AS SmartBorderBboxHeight,
    JSON_VALUE(e.Payload, '$.geometry.smartBorder.rect.width') AS SmartBorderRectWidth,
    JSON_VALUE(e.Payload, '$.geometry.smartBorder.rect.height') AS SmartBorderRectHeight,
    
    -- Full payload (for detailed inspection)
    e.Payload AS FullPayload
    
FROM log.FrontendEvent e
WHERE e.EventType = 'resize.capture'
    AND (@ComponentID IS NULL OR e.ComponentID = @ComponentID)
    AND e.CreatedDate >= DATEADD(HOUR, -@HoursBack, GETUTCDATE())
ORDER BY 
    e.ComponentID,
    JSON_VALUE(e.Payload, '$.captureRunId'),
    CASE JSON_VALUE(e.Payload, '$.phase')
        WHEN 'start.beforeGrab' THEN 1
        WHEN 'start.afterGrab' THEN 2
        WHEN 'sample' THEN 3
        WHEN 'beforeDrop' THEN 4
        WHEN 'afterDrop' THEN 5
        ELSE 99
    END,
    CAST(JSON_VALUE(e.Payload, '$.sampleIndex') AS INT);
