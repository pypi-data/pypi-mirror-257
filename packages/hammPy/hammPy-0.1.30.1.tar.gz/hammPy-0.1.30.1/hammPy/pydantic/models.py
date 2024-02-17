
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
    content: str = Field(..., description="STR")

class ContentModel_INT(BaseModel):
    content: int = Field(..., description="INT")

class listModel_STR(BaseModel):
    list: list[str] = Field(..., description="STR")

class listModel_INT(BaseModel):
    list: list[int] = Field(..., description="INT")

class DoublelistModel_STR(BaseModel):
    list: list[str] = Field(..., description="STR")
    list: list[str] = Field(..., description="STR")

class DoublelistModel_INT(BaseModel):
    list: list[int] = Field(..., description="INT")
    list: list[int] = Field(..., description="INT")

class TriplelistModel_STR(BaseModel):
    list: list[str] = Field(..., description="STR")
    list: list[str] = Field(..., description="STR")
    list: list[str] = Field(..., description="STR")

class TriplelistModel_INT(BaseModel):
    list: list[int] = Field(..., description="INT")
    list: list[int] = Field(..., description="INT")
    list: list[int] = Field(..., description="INT")

class NestedlistModel_STR(BaseModel):
    list: list[list[str]] = Field(..., description="NESTED STR")
    list: list[list[str]] = Field(..., description="NESTED STR")

class NestedlistModel_INT(BaseModel):
    list: list[list[int]] = Field(..., description="NESTED INT")
    list: list[list[int]] = Field(..., description="NESTED INT")

class NestedlistModel_INTSTR(BaseModel):
    list: list[list[int]] = Field(..., description="NESTED INT")
    list: list[list[str]] = Field(..., description="NESTED STR")

class DoubleNestedlistModel_STRSTR(BaseModel):
    list: list[str] = Field(..., description="STR")
    list: list[str] = Field(..., description="STR")
    list: list[list[str]] = Field(..., description="NESTED STR")
    list: list[list[str]] = Field(..., description="NESTED STR")

class DoubleNestedlistModel_INTSTR(BaseModel):
    list: list(int) = Field(..., description="INT")
    list: list(str) = Field(..., description="STR")
    list: list[list[int]] = Field(..., description="NESTED INTR")
    list: list[list[str]] = Field(..., description="NESTED STR")



