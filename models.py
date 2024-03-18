from pydantic import BaseModel, Field, field_validator, ValidationInfo
from uuid import UUID, uuid4
from typing import Optional, List
from enum import Enum


class ComStyle(str, Enum):
    criticism = 'criticism'
    contempt = 'contempt'
    defensiveness = 'defensiveness'
    stonewalling = 'stonewalling'
    neutral = 'neutral'
    unclear = 'unclear'


class TextModel(BaseModel):
    id: UUID = Field(default_factory=uuid4) # id: Optional[UUID] = uuid4()
    original_text: str = Field(min_length=10)
    raw_output: str = Field(default="")
    splitted_text: List[str] = Field(default_factory=list) # original text splitted into sentences
    communication_style: List[ComStyle] = Field(default_factory=list) # communication category of each splitted sentence
    transformed_text: str = Field(default="") # text transformed into neutral/functional language


    @field_validator('communication_style')
    def check_lengths_match(cls, v: str, info: ValidationInfo) -> str:
        """
        A class method that enforces the constraint that the lengths of the splitted_text and 
        communication_style lists must be the same.
        Specifying communication_style as target field tells Pydantic to run this validator
        on the communication_style field whenever a Message instance is created or modified.
        
        Args:
            cls: Refers to the class itself, not an instance of the class. This is common for class methods.
            v: The value of the field being validated (here the list assigned to communication_style).
            info: ValidationInfo.data is a dictionary containing the name-value pairs of any fields of the
                    model that have already been validated.
        
        Returns:
            If no error is raised (i.e., the lengths match), the function returns v (i.e., the unmodified 
            value of communication_style); this is a requirement for Pydantic validators: if a value passes
            validation, it should be returned (it can be transformed).
        """
        if 'splitted_text' in info.data and len(v) != len(info.data['splitted_text']):
            raise ValueError('splitted_text and communication_style must have the same length!')
        return v


class MessageUpdateRequest(BaseModel):
    original_text: Optional[str] = None
    raw_output: Optional[str] = None
    splitted_text: Optional[List[str]] = None
    communication_style: Optional[List[ComStyle]] = None
    transformed_text: Optional[str] = None
