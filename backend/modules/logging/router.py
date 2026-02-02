"""
Logging Router
API endpoints for frontend logging integration
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.logger import get_logger
from models.log.frontend_event import FrontendEvent
from .schemas import FrontendLogBatch, FrontendLogResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/logs", tags=["Logging"])


def extract_component_info(payload: dict) -> tuple:
    """Extract ComponentID and ComponentType from payload"""
    component_id = payload.get("componentId") if payload else None
    component_type = payload.get("componentType") if payload else None
    
    # Also check for nested component object
    if not component_id and payload:
        component = payload.get("component", {})
        if isinstance(component, dict):
            component_id = component.get("id") or component.get("componentId")
            component_type = component.get("type") or component.get("componentType")
    
    return component_id, component_type


def extract_metrics_payload(payload: dict) -> dict | None:
    """Extract metrics snapshot payload for storage."""
    if not payload:
        return None
    if "componentBefore" in payload or "componentAfter" in payload:
        return {
            "before": payload.get("componentBefore"),
            "after": payload.get("componentAfter"),
        }
    if "component" in payload:
        return {"snapshot": payload.get("component")}
    return None


def extract_summary_snapshot(payload: dict) -> dict:
    """Select the best snapshot for summary metrics."""
    if not payload:
        return {}
    if payload.get("componentAfter"):
        return payload.get("componentAfter") or {}
    if payload.get("component"):
        return payload.get("component") or {}
    if payload.get("componentBefore"):
        return payload.get("componentBefore") or {}
    return {}


def parse_metric_number(value) -> int | None:
    if value is None:
        return None
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return None


def summarize_metrics(payload: dict) -> dict:
    """Summarize metrics for fast querying."""
    snapshot = extract_summary_snapshot(payload)
    if not snapshot:
        return {}

    props = snapshot.get("props") or {}
    grid_metrics = snapshot.get("gridMetrics") or {}
    object_metrics = snapshot.get("objectMetrics") or {}
    object_widths = snapshot.get("objectWidths") or {}

    object_ids = list(object_metrics.keys()) or list(object_widths.keys())
    has_validation = "validation" in object_ids if object_ids else False

    layout_type = None
    if grid_metrics or props.get("gridLayout"):
        layout_type = "grid"
    elif props.get("objectLayout") or props.get("layoutGroups"):
        layout_type = "object"

    container_width = parse_metric_number(grid_metrics.get("containerWidth") or (snapshot.get("bounds") or {}).get("width"))
    container_height = parse_metric_number(grid_metrics.get("containerHeight") or (snapshot.get("bounds") or {}).get("height"))

    grid_columns = None
    grid_rows = None
    grid_layout = props.get("gridLayout") or {}
    if isinstance(grid_layout, dict):
        grid_columns = grid_layout.get("columns")
        grid_rows = grid_layout.get("rows")

    if grid_columns is None:
        tracks = grid_metrics.get("templateColumnsPx")
        if isinstance(tracks, list) and tracks:
            grid_columns = int((len(tracks) + 1) / 2)
    if grid_rows is None:
        tracks = grid_metrics.get("templateRowsPx")
        if isinstance(tracks, list) and tracks:
            grid_rows = int((len(tracks) + 1) / 2)

    return {
        "layout_type": layout_type,
        "object_count": len(object_ids) if object_ids else None,
        "container_width": container_width,
        "container_height": container_height,
        "grid_columns": grid_columns,
        "grid_rows": grid_rows,
        "has_validation": bool(has_validation),
    }


@router.post(
    "/frontend",
    response_model=FrontendLogResponse,
    summary="Submit Frontend Logs",
    description="Submit a batch of frontend log entries for storage and analysis. "
                "Used by the devLogger to send builder events to the backend."
)
async def submit_frontend_logs(
    batch: FrontendLogBatch,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Submit frontend log entries.
    
    Accepts a batch of log entries from the frontend devLogger.
    Stores them in log.FrontendEvent for analysis via enhanced_diagnostic_logs.py.
    
    No authentication required - logs may come from unauthenticated sessions.
    User context is captured if available via session/request.
    """
    try:
        # Get user ID from request context if available
        user_id = getattr(request.state, 'user_id', None) if hasattr(request, 'state') else None
        request_id = getattr(request.state, 'request_id', None) if hasattr(request, 'state') else None
        
        stored_count = 0
        
        for entry in batch.entries:
            component_id, component_type = extract_component_info(entry.payload)
            metrics_payload = extract_metrics_payload(entry.payload)
            summary = summarize_metrics(entry.payload)
            
            frontend_event = FrontendEvent(
                EventType=entry.event,
                Level=entry.level,
                ComponentID=component_id,
                ComponentType=component_type,
                Payload=json.dumps(entry.payload) if entry.payload else None,
                MetricsJson=json.dumps(metrics_payload) if metrics_payload else None,
                LayoutType=summary.get("layout_type"),
                ObjectCount=summary.get("object_count"),
                ContainerWidth=summary.get("container_width"),
                ContainerHeight=summary.get("container_height"),
                GridColumns=summary.get("grid_columns"),
                GridRows=summary.get("grid_rows"),
                HasValidationObject=summary.get("has_validation", False),
                SessionID=batch.sessionId,
                UserID=user_id,
                RequestID=request_id,
                BrowserInfo=batch.browserInfo,
                PageURL=batch.pageUrl,
                ClientTimestamp=entry.ts
            )
            db.add(frontend_event)
            stored_count += 1
        
        db.commit()
        
        logger.debug(f"Stored {stored_count} frontend log entries for SessionID {batch.sessionId}")
        
        return FrontendLogResponse(
            received=len(batch.entries),
            stored=stored_count,
            message="OK"
        )
        
    except Exception as e:
        logger.error(f"Error storing frontend logs: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error storing logs: {str(e)}"
        )


@router.get(
    "/frontend/recent",
    summary="Get Recent Frontend Logs",
    description="Get recent frontend log entries (for debugging). "
                "Primarily used by enhanced_diagnostic_logs.py."
)
async def get_recent_frontend_logs(
    limit: int = 50,
    session_id: str = None,
    component_id: str = None,
    event_filter: str = None,
    level: str = None,
    db: Session = Depends(get_db)
):
    """
    Get recent frontend log entries.
    
    Query Parameters:
    - limit: Maximum entries to return (default 50)
    - session_id: Filter by session ID
    - component_id: Filter by component ID
    - event_filter: Filter by event type (partial match)
    - level: Filter by log level
    """
    from sqlalchemy import desc
    
    query = db.query(FrontendEvent)
    
    if session_id:
        query = query.filter(FrontendEvent.SessionID == session_id)
    if component_id:
        query = query.filter(FrontendEvent.ComponentID == component_id)
    if event_filter:
        query = query.filter(FrontendEvent.EventType.like(f"%{event_filter}%"))
    if level:
        query = query.filter(FrontendEvent.Level == level)
    
    events = query.order_by(desc(FrontendEvent.CreatedDate)).limit(limit).all()
    
    return {
        "count": len(events),
        "events": [
            {
                "id": e.FrontendEventID,
                "eventType": e.EventType,
                "level": e.Level,
                "componentId": e.ComponentID,
                "componentType": e.ComponentType,
                "payload": json.loads(e.Payload) if e.Payload else None,
                "metrics": json.loads(e.MetricsJson) if e.MetricsJson else None,
                "layoutType": e.LayoutType,
                "objectCount": e.ObjectCount,
                "containerWidth": e.ContainerWidth,
                "containerHeight": e.ContainerHeight,
                "gridColumns": e.GridColumns,
                "gridRows": e.GridRows,
                "hasValidationObject": bool(e.HasValidationObject),
                "sessionId": e.SessionID,
                "pageUrl": e.PageURL,
                "clientTimestamp": e.ClientTimestamp,
                "createdDate": e.CreatedDate.isoformat() if e.CreatedDate else None
            }
            for e in events
        ]
    }











