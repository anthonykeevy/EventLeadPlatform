from typing import Dict, Any
from fastapi import HTTPException
from pydantic import ValidationError
from schemas.form_definition import FormDefinition

def validate_definition(data: Dict[str, Any]) -> FormDefinition:
    """
    Validates the form definition JSON against the Pydantic schema.
    Raises HTTPException(400) if invalid.
    """
    try:
        return FormDefinition.model_validate(data)
    except ValidationError as e:
        # Flatten errors for a cleaner response
        error_messages = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error['loc'])
            msg = error['msg']
            error_messages.append(f"{loc}: {msg}")
        
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid Form Definition Schema",
                "errors": error_messages
            }
        )

