from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Position(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None

class Style(BaseModel):
    font_size: Optional[float] = None
    font_family: Optional[str] = None
    color: Optional[str] = None

class Element(BaseModel):
    type: str = Field(..., pattern="^(text|image|shape)$")
    content: Optional[str] = None
    image_url: Optional[str] = None
    position: Optional[Position] = None
    style: Optional[Style] = None

class Slide(BaseModel):
    layout_id: Optional[str] = None
    elements: List[Element]

class PresentationRequest(BaseModel):
    title: str
    template_id: str
    slides: List[Slide]
