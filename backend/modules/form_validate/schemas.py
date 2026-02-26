from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SchemaError(BaseModel):
    path: str
    message: str
    code: str


class BoundaryDirectionFlags(BaseModel):
    left: bool = False
    right: bool = False
    top: bool = False
    bottom: bool = False


class BoundaryViolation(BaseModel):
    componentId: str
    pageId: str
    layout: str
    position: Dict[str, float]
    size: Dict[str, float]
    canvas: Dict[str, float]
    violations: BoundaryDirectionFlags


class CollisionViolation(BaseModel):
    componentAId: str
    componentBId: str
    pageId: str
    layout: str
    overlapArea: float = Field(ge=0.0)


class ValidationSummary(BaseModel):
    errorCount: int
    warningCount: int = 0


class FormValidationResponse(BaseModel):
    valid: bool
    schemaErrors: List[SchemaError]
    boundaryViolations: List[BoundaryViolation]
    collisions: List[CollisionViolation]
    summary: ValidationSummary
    meta: Optional[Dict[str, Any]] = None
