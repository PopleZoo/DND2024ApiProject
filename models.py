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

# Separate Traits models
class AbilityScoreIncrease(BaseModel):
    abilityScoreIncrease: str

class Size(BaseModel):
    size: str

class Speed(BaseModel):
    speed: int

class Languages(BaseModel):
    languages: List[str]

class SpeciesTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    size: Optional[Size] = None
    speed: Optional[Speed] = None
    languages: Optional[Languages] = None

class SubspeciesTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    speed: Optional[Speed] = None
    cantrips: Optional[str] = None
    darkvision: Optional[str] = None

class VariantTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    speed: Optional[Speed] = None
    cantrips: Optional[str] = None
    darkvision: Optional[str] = None


class Variant(BaseModel):
    id: str
    name: str
    description: Optional[str]
    traits: VariantTraits

class Subspecies(BaseModel):
    id: str
    name: str
    description: Optional[str]
    traits: SubspeciesTraits
    variants: Optional[List[Variant]]

class Species(BaseModel):
    id: str
    name: str
    description: Optional[str]
    traits: SpeciesTraits
    subspecies: Optional[List[Subspecies]]