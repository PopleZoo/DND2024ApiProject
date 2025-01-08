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
    level: Optional[int] = None  # Optional, some classes may not have levels set initially
    hitDice: int
    isStartingClass: bool
    isHomebrew: bool
    definition: Optional[Dict[str, Any]] = None  # Flexible, can be expanded as needed
    subclasses: List[Subclass]  # List of subclasses for the class

# Separate Traits models

# Represents ability score increase, e.g., +2 to Strength
class AbilityScoreIncrease(BaseModel):
    abilityScoreIncrease: str

# Represents the size category of a species or variant (e.g., Small, Medium, Large)
class Size(BaseModel):
    size: str

# Represents movement speed (e.g., 30 feet)
class Speed(BaseModel):
    speed: int

# Represents a list of languages a species or variant knows
class Languages(BaseModel):
    languages: List[str]

# Traits that apply to a species
class SpeciesTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    size: Optional[Size] = None
    speed: Optional[Speed] = None
    languages: Optional[Languages] = None

# Traits specific to subspecies
class SubspeciesTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    speed: Optional[Speed] = None
    cantrips: Optional[str] = None  # Additional spells or abilities for the subspecies
    darkvision: Optional[str] = None  # Darkvision trait for the subspecies

# Traits specific to a variant
class VariantTraits(BaseModel):
    abilityScoreIncrease: Optional[AbilityScoreIncrease] = None
    speed: Optional[Speed] = None
    cantrips: Optional[str] = None
    darkvision: Optional[str] = None

# Represents a variant of a species
class Variant(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    traits: VariantTraits

# Represents a subspecies of a species
class Subspecies(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    traits: SubspeciesTraits  # Traits specific to this subspecies
    variants: Optional[List[Variant]] = []  # A list of variants, optional if none exist

# Main Species model representing a species and its subspecies
class Species(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    traits: SpeciesTraits  # Traits common to the species
    subspecies: Optional[List[Subspecies]] = []  # List of subspecies for this species
