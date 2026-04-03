from typing import Annotated, Dict, List

from pydantic import BaseModel, Field, RootModel

class ConntectionMessageSchemas(BaseModel):
    message: Annotated[str, Field(max_length=1000)]
    
    

class MessageResponse(RootModel[Dict[str, List[Dict[str, str]]]]):
    pass