from pydantic import BaseModel, Field, field_validator, ValidationInfo
from uuid import UUID, uuid4
from typing import Optional #, List
# from enum import Enum


# class ComStyle(str, Enum):
#     criticism = 'criticism'
#     contempt = 'contempt'
#     defensiveness = 'defensiveness'
#     stonewalling = 'stonewalling'
#     neutral = 'neutral'
#     unclear = 'unclear'


class TextModel(BaseModel):
    id: UUID = Field(default_factory=uuid4) # id: Optional[UUID] = uuid4()
    original_text: str = Field(min_length=10)
    prompt: str = Field(default="") # prompt to pass to the LLM
    # raw_output: str = Field(default="")
    # splitted_text: List[str] = Field(default_factory=list) # original text splitted into sentences
    # communication_style: List[ComStyle] = Field(default_factory=list) # communication category of each splitted sentence
    transformed_text: str = Field(default="") # text transformed into neutral/functional language

    
    @field_validator("original_text")
    @classmethod
    def check_string(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Args:
            cls: Refers to the class itself, not an instance of the class. This is common for class methods.
            v: The value of the field being validated.
            info: ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
                    model that have already been validated.
        
        Returns:
            If no error is raised (i.e., the field is validated), the function returns v (i.e., the unmodified 
            value of of the field); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if not isinstance(v, str):
            raise ValueError("original_text must be a string")
        return v
    

    @field_validator("prompt")
    @classmethod
    def check_string(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Args:
            cls: Refers to the class itself, not an instance of the class. This is common for class methods.
            v: The value of the field being validated.
            info: ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
                    model that have already been validated.
        
        Returns:
            If no error is raised (i.e., the field is validated), the function returns v (i.e., the unmodified 
            value of of the field); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if not isinstance(v, str):
            raise ValueError("prompt must be a string")
        return v
    

    @field_validator("transformed_text")
    @classmethod
    def check_string(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces a constraint about a filed in the class.
        
        Args:
            cls: Refers to the class itself, not an instance of the class. This is common for class methods.
            v: The value of the field being validated.
            info: ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
                    model that have already been validated.
        
        Returns:
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
    # raw_output: Optional[str] = None
    # splitted_text: Optional[List[str]] = None
    # communication_style: Optional[List[ComStyle]] = None
    transformed_text: Optional[str] = None
