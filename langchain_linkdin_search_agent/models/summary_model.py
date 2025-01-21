from typing import Any
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class Summary(BaseModel):
    summary: str = Field(description = "A Short Summary About Linkedin Profile")
    facts: list[str] = Field(description = "Interesting Facts About User Profile")
    
    def to_dict(self):
        return {"summary": self.summary, "facts": self.facts}


class Agent_Response(BaseModel):
    summary: Summary = Field(description="Summary and facts about the LinkedIn profile")
    profile_pic_url: str = Field(description = "URL of the Profile Picture")
    
    
    
summary = PydanticOutputParser(pydantic_object = Summary)