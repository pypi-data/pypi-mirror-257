
#==============================================================================#
#== Hammad Saeed ==============================================================#
#==============================================================================#
#== www.hammad.fun ============================================================#
#== hammad@supportvectors.com =================================================#
#==============================================================================#

##== HamPy ==######################################== Hammad's Python Tools ==##
##== @/pydantic/models ==#######################################################
##== Pydantic Models ==#########################################################

#==============================================================================#

from pydantic import BaseModel, Field

#==============================================================================#


class ContentModel_STR(BaseModel):
    content: str = Field

class ContentModel_INT(BaseModel):
    content: int = Field

class listModel_STR(BaseModel):
    list: list[str] = Field

class listModel_INT(BaseModel):
    list: list[int] = Field

class DoublelistModel_STR(BaseModel):
    list: list[str] = Field
    list: list[str] = Field

class DoublelistModel_INT(BaseModel):
    list: list[int] = Field
    list: list[int] = Field

class TriplelistModel_STR(BaseModel):
    list: list[str] = Field
    list: list[str] = Field
    list: list[str] = Field

class TriplelistModel_INT(BaseModel):
    list: list[int] = Field
    list: list[int] = Field
    list: list[int] = Field

class NestedlistModel_STR(BaseModel):
    list: list[list[str]] = Field
    list: list[list[str]] = Field

class NestedlistModel_INT(BaseModel):
    list: list[list[int]] = Field
    list: list[list[int]] = Field

class NestedlistModel_INTSTR(BaseModel):
    list: list[list[int]] = Field
    list: list[list[str]] = Field

class DoubleNestedlistModel_STRSTR(BaseModel):
    list: list[str] = Field
    list: list[str] = Field
    list: list[list[str]] = Field
    list: list[list[str]] = Field

class DoubleNestedlistModel_INTSTR(BaseModel):
    list: list(int) = Field
    list: list(str) = Field
    list: list[list[int]] = Field
    list: list[list[str]] = Field



