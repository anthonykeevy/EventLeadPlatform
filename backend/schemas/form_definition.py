from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator
from enum import Enum

class ComponentType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    DATE = "date"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXTAREA = "textarea"

class FormTheme(BaseModel):
    primaryColor: str = Field(default="#000000")
    backgroundColor: str = Field(default="#FFFFFF")
    fontFamily: str = Field(default="Arial")

class ComponentProps(BaseModel):
    label: str = Field(..., min_length=1)
    required: bool = False
    placeholder: Optional[str] = None
    # Allow extra fields for specific component types (e.g., options for select)
    model_config = {"extra": "allow"}

class FormComponent(BaseModel):
    id: str = Field(..., min_length=1)
    type: ComponentType
    props: ComponentProps

class FormPage(BaseModel):
    id: str = Field(..., min_length=1)
    title: Optional[str] = None
    components: List[FormComponent] = Field(default_factory=list)

class LogicOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    CONTAINS = "contains"
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
    operator: LogicOperator
    value: Optional[str] = None

    @model_validator(mode="after")
    def validate_value_requirements(self) -> "RuleWhen":
        if self.operator == LogicOperator.IS_EMPTY:
            # value not used for isEmpty
            self.value = None
            return self
        if self.operator in (LogicOperator.EQUALS, LogicOperator.NOT_EQUALS, LogicOperator.CONTAINS):
            if self.value is None or str(self.value).strip() == "":
                raise ValueError(f"value is required for operator '{self.operator.value}'")
        return self

class RuleThen(BaseModel):
    targetComponentId: str = Field(..., min_length=1)
    action: LogicAction

class LogicRule(BaseModel):
    id: str = Field(..., min_length=1)
    enabled: bool = True
    name: Optional[str] = None
    when: RuleWhen
    then: RuleThen

class FormLogic(BaseModel):
    rules: List[LogicRule] = Field(default_factory=list)

class FormDefinition(BaseModel):
    schemaVersion: Literal["1.0"] = "1.0"
    formId: str = Field(..., min_length=1)
    theme: FormTheme
    pages: List[FormPage]
    # Story 3.6: Rule definitions stored as structured JSON (no code)
    logic: Optional[FormLogic] = None

    @model_validator(mode='after')
    def check_unique_ids(self) -> 'FormDefinition':
        """
        Validate that all component IDs are unique across the entire form.
        """
        seen_ids = set()
        duplicates = []

        for page in self.pages:
            for component in page.components:
                if component.id in seen_ids:
                    duplicates.append(component.id)
                seen_ids.add(component.id)
        
        if duplicates:
            raise ValueError(f"Duplicate component IDs found: {', '.join(duplicates)}")

        # Optional rule integrity checks (structure-only; runtime evaluation is Story 3.7)
        if self.logic and self.logic.rules:
            for rule in self.logic.rules:
                if rule.when.sourceComponentId == rule.then.targetComponentId:
                    raise ValueError("Rule sourceComponentId cannot equal targetComponentId")
        
        return self

