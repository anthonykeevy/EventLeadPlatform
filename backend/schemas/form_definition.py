"""
Form Definition Schema - Story 5.3 Schema + Validation Alignment
Aligns with DefinitionJSON produced by Form Builder (builder.types.ts).
Validates full structure: theme, globalStyles, canvasSettings, logic, pages,
desktopPages/tabletPages/mobilePages, FormPage.background, component structure.
"""
from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, model_validator, model_serializer
from enum import Enum


# ─── Component types (align with builder.types.ts ComponentType) ───
class ComponentType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    URL = "url"
    SELECT = "select"
    DROPDOWN = "dropdown"
    DATE = "date"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXTAREA = "textarea"
    EMAIL = "email"
    PHONE = "phone"
    RATING = "rating"
    ADDRESS = "address"
    FIRST_NAME = "first-name"
    TERMS = "terms"
    SUBMIT_BUTTON = "submit-button"
    HEADER = "header"
    PARAGRAPH = "paragraph"
    DIVIDER = "divider"
    ROW = "row"
    COLUMN = "column"


# ─── FormTheme ───
class FormTheme(BaseModel):
    primaryColor: str = Field(default="#000000")
    backgroundColor: str = Field(default="#FFFFFF")
    fontFamily: str = Field(default="Arial")


# ─── ComponentProps: per-component props; allow extra for extensibility ───
class ComponentProps(BaseModel):
    label: Optional[str] = None
    required: bool = False
    placeholder: Optional[str] = None
    helpText: Optional[str] = None
    styleOverrides: Optional[Dict[str, Any]] = None
    validation: Optional[Dict[str, Any]] = None
    options: Optional[List[Dict[str, Any]]] = None
    model_config = {"extra": "allow"}


# ─── Position (canvas) ───
class ComponentPosition(BaseModel):
    x: float = 0.0
    y: float = 0.0


# ─── Style (zIndex, width, height) ───
class ComponentStyle(BaseModel):
    zIndex: Optional[int] = None
    width: Optional[float] = None
    height: Optional[float] = None


# ─── GridLayoutConfig (partial; full def in builder.types) ───
class GridLayoutConfig(BaseModel):
    rows: Optional[int] = None
    columns: Optional[int] = None
    columnGap: Optional[int] = None
    rowGap: Optional[int] = None
    cellAssignments: Optional[Dict[str, str]] = None
    mergedCells: Optional[Dict[str, Any]] = None
    objectSpans: Optional[Dict[str, Any]] = None
    model_config = {"extra": "allow"}


# ─── FormComponent (recursive via children) ───
# type: str to accept any component type from builder (paragraph, row, column, etc.)
class FormComponent(BaseModel):
    id: str = Field(..., min_length=1)
    type: str
    props: ComponentProps = Field(default_factory=ComponentProps)
    position: Optional[ComponentPosition] = None
    style: Optional[ComponentStyle] = None
    styleOverrides: Optional[Dict[str, Any]] = None
    children: Optional[List["FormComponent"]] = None
    gridLayout: Optional[Union[GridLayoutConfig, Dict[str, Any], type(None)]] = None
    model_config = {"extra": "forbid"}


# Resolve forward reference
FormComponent.model_rebuild()


# ─── Background (Story 5.1: color | image, asset ref) ───
class BackgroundPlacement(BaseModel):
    position: Optional[Dict[str, float]] = None
    size: Optional[Dict[str, float]] = None
    crop: Optional[Dict[str, float]] = None
    model_config = {"extra": "allow"}


class BackgroundDefinition(BaseModel):
    type: Literal["color", "image"] = "color"
    value: Optional[str] = None
    colorValue: Optional[str] = None
    asset: Optional[Dict[str, Any]] = None
    placement: Optional[BackgroundPlacement] = None
    imageSize: Optional[str] = None
    lockAspectRatio: Optional[bool] = None
    overlayColor: Optional[str] = None
    overlayOpacity: Optional[float] = None
    opacity: Optional[float] = None
    model_config = {"extra": "allow"}


# ─── FormPage ───
class FormPage(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = ""
    components: List[FormComponent] = Field(default_factory=list)
    background: Optional[BackgroundDefinition] = None
    model_config = {"extra": "forbid"}


# ─── Logic (Story 3.6) ───
class LogicOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    CONTAINS = "contains"
    GREATER_THAN = "greaterThan"
    GREATER_THAN_OR_EQUAL = "greaterThanOrEqual"
    LESS_THAN = "lessThan"
    LESS_THAN_OR_EQUAL = "lessThanOrEqual"
    IS_EMPTY = "isEmpty"


class LogicAction(str, Enum):
    SHOW = "show"
    HIDE = "hide"
    REQUIRE = "require"
    UNREQUIRE = "unrequire"
    ENABLE = "enable"
    DISABLE = "disable"


class RuleWhen(BaseModel):
    sourceComponentId: str = Field(..., min_length=1)
    operator: str  # equals, notEquals, contains, isEmpty, etc.
    value: Optional[str] = None

    @model_serializer(mode="wrap")
    def serialize_rule_when(self, serializer, info):
        data = serializer(self)
        if str(self.operator) == "isEmpty":
            data.pop("value", None)
        return data

    @model_validator(mode="after")
    def validate_value_requirements(self) -> "RuleWhen":
        if str(self.operator) == "isEmpty":
            self.value = None
            return self
        if str(self.operator) in ("equals", "notEquals", "contains"):
            if self.value is None or str(self.value).strip() == "":
                raise ValueError(f"value is required for operator '{self.operator}'")
        return self


class RuleThen(BaseModel):
    targetComponentId: str = Field(..., min_length=1)
    action: str  # show, hide, require, etc.


class LogicRule(BaseModel):
    id: str = Field(..., min_length=1)
    enabled: bool = True
    name: Optional[str] = None
    when: RuleWhen
    then: RuleThen


class FormLogic(BaseModel):
    rules: List[LogicRule] = Field(default_factory=list)


# ─── GlobalStyles: 30+ fields; define key structure, allow extra ───
class GlobalStyles(BaseModel):
    fontFamily: Optional[str] = None
    fontSize: Optional[int] = None
    fontWeight: Optional[int] = None
    fontStyle: Optional[str] = None
    labelFontFamily: Optional[str] = None
    labelFontSize: Optional[int] = None
    labelFontWeight: Optional[int] = None
    labelFontStyle: Optional[str] = None
    helpTextFontFamily: Optional[str] = None
    helpTextFontSize: Optional[int] = None
    helpTextFontWeight: Optional[int] = None
    helpTextFontStyle: Optional[str] = None
    textColor: Optional[str] = None
    textBackgroundColor: Optional[str] = None
    labelColor: Optional[str] = None
    labelBackgroundColor: Optional[str] = None
    helpTextColor: Optional[str] = None
    helpTextBackgroundColor: Optional[str] = None
    actionFontFamily: Optional[str] = None
    actionFontSize: Optional[int] = None
    actionFontWeight: Optional[int] = None
    actionFontStyle: Optional[str] = None
    actionTextColor: Optional[str] = None
    actionBackgroundColor: Optional[str] = None
    actionBorderColor: Optional[str] = None
    actionBorderWidth: Optional[int] = None
    actionBorderRadius: Optional[int] = None
    dividerBorderColor: Optional[str] = None
    dividerBorderWidth: Optional[int] = None
    dividerWidth: Optional[str] = None
    primaryColor: Optional[str] = None
    placeholderColor: Optional[str] = None
    backgroundColor: Optional[str] = None
    borderColor: Optional[str] = None
    errorColor: Optional[str] = None
    baseSpacing: Optional[int] = None
    labelGap: Optional[float] = None
    inputHelpGap: Optional[float] = None
    inputPaddingX: Optional[float] = None
    inputPaddingY: Optional[float] = None
    objectRowGapPx: Optional[int] = None
    objectColumnGapPx: Optional[int] = None
    borderRadius: Optional[int] = None
    borderWidth: Optional[int] = None
    inputHeight: Optional[int] = None
    defaultLayout: Optional[str] = None
    defaultObjectLayout: Optional[str] = None
    defaultLayoutGroups: Optional[Dict[str, list]] = None
    defaultGridLayout: Optional[Dict[str, Any]] = None
    defaultGridLayoutsByComponent: Optional[Dict[str, Any]] = None
    model_config = {"extra": "allow"}


# ─── CanvasSettings ───
class CanvasSettings(BaseModel):
    width: int = 1920
    height: int = 980
    gridSize: int = 8
    backgroundColor: Optional[str] = None
    model_config = {"extra": "forbid"}


# ─── FormDefinition ───
class FormDefinition(BaseModel):
    schemaVersion: Literal["1.0"] = "1.0"
    formId: str = Field(..., min_length=1)
    theme: FormTheme
    pages: List[FormPage] = Field(..., min_length=1)
    globalStyles: Optional[GlobalStyles] = None
    logic: Optional[FormLogic] = None
    canvasSettings: Optional[CanvasSettings] = None
    desktopPages: Optional[List[FormPage]] = None
    tabletPages: Optional[List[FormPage]] = None
    mobilePages: Optional[List[FormPage]] = None
    model_config = {"extra": "forbid"}

    def _collect_component_ids(self, pages: Optional[List[FormPage]]) -> List[str]:
        ids: List[str] = []
        if not pages:
            return ids
        for page in pages:
            for comp in page.components:
                ids.append(comp.id)
                if comp.children:
                    ids.extend(self._collect_from_children(comp.children))
        return ids

    def _collect_from_children(self, children: List[FormComponent]) -> List[str]:
        ids: List[str] = []
        for comp in children:
            ids.append(comp.id)
            if comp.children:
                ids.extend(self._collect_from_children(comp.children))
        return ids

    def _ids_in_page(self, page: FormPage) -> List[str]:
        ids: List[str] = []
        for comp in page.components:
            ids.append(comp.id)
            if comp.children:
                ids.extend(self._collect_from_children(comp.children))
        return ids

    @model_validator(mode="after")
    def check_unique_ids(self) -> "FormDefinition":
        """Unique component IDs within each page array (pages, desktopPages, etc.).
        Same ID may appear in pages and desktopPages (same component, different layout)."""
        duplicates: List[str] = []

        def check_pages(pages: List[FormPage], label: str) -> None:
            seen: set = set()
            for page in pages:
                for cid in self._ids_in_page(page):
                    if cid in seen:
                        duplicates.append(cid)
                    seen.add(cid)

        check_pages(self.pages, "pages")
        if self.desktopPages:
            check_pages(self.desktopPages, "desktopPages")
        if self.tabletPages:
            check_pages(self.tabletPages, "tabletPages")
        if self.mobilePages:
            check_pages(self.mobilePages, "mobilePages")

        if duplicates:
            raise ValueError(f"Duplicate component IDs found: {', '.join(duplicates)}")

        if self.logic and self.logic.rules:
            for rule in self.logic.rules:
                if rule.when.sourceComponentId == rule.then.targetComponentId:
                    raise ValueError(
                        "Logic rule: sourceComponentId cannot equal targetComponentId"
                    )

        return self
