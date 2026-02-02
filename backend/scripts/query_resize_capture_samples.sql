-- SQL Query to view detailed sample-by-sample progression for resize captures
-- Shows each sample event with size changes and mouse deltas
-- Useful for debugging specific resize operations
--
-- Usage:
--   1. Set @CaptureRunId to the specific run you want to analyze
--   2. Or set @ComponentID and @Handle to see latest run for that handle

DECLARE @CaptureRunId NVARCHAR(100) = NULL;  -- Set to specific captureRunId, or NULL to use ComponentID/Handle
DECLARE @ComponentID NVARCHAR(100) = NULL;  -- Used if @CaptureRunId is NULL
DECLARE @Handle NVARCHAR(10) = NULL;        -- Used if @CaptureRunId is NULL (e.g., 'n', 's', 'w', 'e', 'ne', 'se', 'nw', 'sw')
DECLARE @HoursBack INT = 2;

WITH CaptureEvents AS (
    SELECT 
        e.FrontendEventID,
        e.CreatedDate,
        e.ComponentID,
        JSON_VALUE(e.Payload, '$.captureRunId') AS CaptureRunId,
        JSON_VALUE(e.Payload, '$.phase') AS Phase,
        JSON_VALUE(e.Payload, '$.handle') AS Handle,
        CAST(JSON_VALUE(e.Payload, '$.sampleIndex') AS INT) AS SampleIndex,
        CAST(JSON_VALUE(e.Payload, '$.mouse.client.x') AS FLOAT) AS MouseX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.client.y') AS FLOAT) AS MouseY,
        CAST(JSON_VALUE(e.Payload, '$.mouse.start.x') AS FLOAT) AS MouseStartX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.start.y') AS FLOAT) AS MouseStartY,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.x') AS FLOAT) AS DeltaFromPrevX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromPrev.y') AS FLOAT) AS DeltaFromPrevY,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromStart.x') AS FLOAT) AS DeltaFromStartX,
        CAST(JSON_VALUE(e.Payload, '$.mouse.deltaFromStart.y') AS FLOAT) AS DeltaFromStartY,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.bounds.width') AS FLOAT) AS BoundsWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.bounds.height') AS FLOAT) AS BoundsHeight,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.smartBorderBounds.width') AS FLOAT) AS SmartBorderWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.smartBorderBounds.height') AS FLOAT) AS SmartBorderHeight,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.width') AS FLOAT) AS InputWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.rect.height') AS FLOAT) AS InputHeight,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.isTextWrapped') AS BIT) AS InputIsWrapped,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.scrollWidth') AS FLOAT) AS InputScrollWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.clientWidth') AS FLOAT) AS InputClientWidth,
        CAST(JSON_VALUE(e.Payload, '$.snapshot.objectMetrics.input.lineCount') AS INT) AS InputLineCount
    FROM log.FrontendEvent e
    WHERE e.EventType = 'resize.capture'
        AND e.CreatedDate >= DATEADD(HOUR, -@HoursBack, GETUTCDATE())
        AND (
            (@CaptureRunId IS NOT NULL AND JSON_VALUE(e.Payload, '$.captureRunId') = @CaptureRunId)
            OR (@CaptureRunId IS NULL AND @ComponentID IS NOT NULL AND @Handle IS NOT NULL 
                AND e.ComponentID = @ComponentID AND JSON_VALUE(e.Payload, '$.handle') = @Handle)
        )
),
OrderedEvents AS (
    SELECT 
        *,
        LAG(BoundsWidth) OVER (PARTITION BY CaptureRunId ORDER BY 
            CASE Phase
                WHEN 'start.beforeGrab' THEN 1
                WHEN 'start.afterGrab' THEN 2
                WHEN 'sample' THEN 3
                WHEN 'beforeDrop' THEN 4
                WHEN 'afterDrop' THEN 5
                ELSE 99
            END,
            SampleIndex
        ) AS PrevBoundsWidth,
        LAG(BoundsHeight) OVER (PARTITION BY CaptureRunId ORDER BY 
            CASE Phase
                WHEN 'start.beforeGrab' THEN 1
                WHEN 'start.afterGrab' THEN 2
                WHEN 'sample' THEN 3
                WHEN 'beforeDrop' THEN 4
                WHEN 'afterDrop' THEN 5
                ELSE 99
            END,
            SampleIndex
        ) AS PrevBoundsHeight,
        LAG(InputWidth) OVER (PARTITION BY CaptureRunId ORDER BY 
            CASE Phase
                WHEN 'start.beforeGrab' THEN 1
                WHEN 'start.afterGrab' THEN 2
                WHEN 'sample' THEN 3
                WHEN 'beforeDrop' THEN 4
                WHEN 'afterDrop' THEN 5
                ELSE 99
            END,
            SampleIndex
        ) AS PrevInputWidth,
        LAG(InputHeight) OVER (PARTITION BY CaptureRunId ORDER BY 
            CASE Phase
                WHEN 'start.beforeGrab' THEN 1
                WHEN 'start.afterGrab' THEN 2
                WHEN 'sample' THEN 3
                WHEN 'beforeDrop' THEN 4
                WHEN 'afterDrop' THEN 5
                ELSE 99
            END,
            SampleIndex
        ) AS PrevInputHeight,
        LAG(InputIsWrapped) OVER (PARTITION BY CaptureRunId ORDER BY 
            CASE Phase
                WHEN 'start.beforeGrab' THEN 1
                WHEN 'start.afterGrab' THEN 2
                WHEN 'sample' THEN 3
                WHEN 'beforeDrop' THEN 4
                WHEN 'afterDrop' THEN 5
                ELSE 99
            END,
            SampleIndex
        ) AS PrevInputIsWrapped
    FROM CaptureEvents
    WHERE CaptureRunId IS NOT NULL
)
SELECT 
    CaptureRunId,
    ComponentID,
    Handle,
    Phase,
    SampleIndex,
    CreatedDate,
    -- Mouse position
    MouseX,
    MouseY,
    MouseStartX,
    MouseStartY,
    DeltaFromPrevX,
    DeltaFromPrevY,
    DeltaFromStartX,
    DeltaFromStartY,
    -- Bounds size and change
    BoundsWidth,
    BoundsWidth - PrevBoundsWidth AS DeltaBoundsWidth,
    BoundsHeight,
    BoundsHeight - PrevBoundsHeight AS DeltaBoundsHeight,
    -- SmartBorder size
    SmartBorderWidth,
    SmartBorderHeight,
    -- Input size and change
    InputWidth,
    InputWidth - PrevInputWidth AS DeltaInputWidth,
    InputHeight,
    InputHeight - PrevInputHeight AS DeltaInputHeight,
    -- Input wrapping status
    InputIsWrapped,
    CASE WHEN PrevInputIsWrapped = 0 AND InputIsWrapped = 1 THEN 1 ELSE 0 END AS WrapFlip,
    InputScrollWidth,
    InputClientWidth,
    InputLineCount
FROM OrderedEvents
ORDER BY 
    CaptureRunId,
    CASE Phase
        WHEN 'start.beforeGrab' THEN 1
        WHEN 'start.afterGrab' THEN 2
        WHEN 'sample' THEN 3
        WHEN 'beforeDrop' THEN 4
        WHEN 'afterDrop' THEN 5
        ELSE 99
    END,
    SampleIndex;
