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

class FormDefinition(BaseModel):
    schemaVersion: Literal["1.0"] = "1.0"
    formId: str = Field(..., min_length=1)
    theme: FormTheme
    pages: List[FormPage]

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
        
        return self

