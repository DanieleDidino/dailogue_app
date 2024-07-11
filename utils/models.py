from pydantic import BaseModel, Field, field_validator, ValidationInfo
from uuid import UUID, uuid4
from typing import Optional


class TextModel(BaseModel):
    id: UUID = Field(default_factory=uuid4) # id: Optional[UUID] = uuid4()
    original_text: str = Field(min_length=10)
    prompt: str = Field(default="") # prompt to pass to the LLM
    transformed_text: str = Field(default="") # text transformed into neutral/functional language

    
    @field_validator("original_text")
    @classmethod
    def check_original_text(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Parameters:
        -----------
        cls: 
            Refers to the class itself, not an instance of the class. This is common for class methods.
        v: str
            The value of the field being validated.
        info: ValidationInfo
            ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
            model that have already been validated.
        
        Returns:
        -----------
        str
            If no error is raised (i.e., the field is validated), the function returns v (i.e., the unmodified 
            value of of the field); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if not isinstance(v, str):
            raise ValueError("original_text must be a string")
        return v
    

    @field_validator("prompt")
    @classmethod
    def check_prompt(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Parameters:
        -----------
        cls:
            Refers to the class itself, not an instance of the class. This is common for class methods.
        v: str
            The value of the field being validated.
        info: ValidationInfo
            ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
            model that have already been validated.
        
        Returns:
        -----------
        str
            If no error is raised (i.e., the field is validated), the function returns v (i.e., the unmodified 
            value of of the field); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if not isinstance(v, str):
            raise ValueError("prompt must be a string")
        return v
    

    @field_validator("transformed_text")
    @classmethod
    def check_transformed_text(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Parameters:
        -----------
        cls:
            Refers to the class itself, not an instance of the class. This is common for class methods.
        v: str
            The value of the field being validated.
        info: ValidationInfo
            ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
            model that have already been validated.
        
        Returns:
        -----------
        str
            If no error is raised (i.e., the field is validated), the function returns v (i.e., the unmodified 
            value of of the field); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if not isinstance(v, str):
            raise ValueError("transformed_text must be a string")
        return v


class MessageUpdateRequest(BaseModel):
    original_text: Optional[str] = None
    prompt: Optional[str] = None
    transformed_text: Optional[str] = None
