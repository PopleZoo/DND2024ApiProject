from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# ClassFeature represents the features of a class.
class ClassFeature(BaseModel):
    id: str
    name: str
    description: str
    level: int
    isHomebrew: bool

# Subclass represents a specific subclass of a class.
class Subclass(BaseModel):
    id: str
    name: str
    description: str
    features: List[ClassFeature]

# Class represents a D&D class with optional definition for flexibility.
class Class(BaseModel):
    id: str
    name: str
    level: Optional[int] = None  # Optional as some classes might not have levels set immediately
    hitDice: int
    isStartingClass: bool
    isHomebrew: bool
    definition: Optional[Dict[str, Any]] = None  # Optional and can be expanded based on specific definition fields
    subclasses: List[Subclass]  # List of subclasses for the class


class Traits(BaseModel):
    breathWeapon: Optional[str]
    damageResistance: Optional[str]

class Variant(BaseModel):
    id: str
    name: str
    description: Optional[str]
    traits: Traits

class Subspecies(BaseModel):
    id: str
    name: str
    description: Optional[str]
    variants: Optional[List[Variant]]

class Species(BaseModel):
    id: str
    name: str
    description: Optional[str]
    traits: Traits
    subspecies: Optional[List[Subspecies]]