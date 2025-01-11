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

class Trait(BaseModel):
    name: str
    description: str

# Traits that apply to a species
class SpeciesTraits(BaseModel):
    abilityScoreIncrease: Optional[str] = None
    size: Optional[int] = None
    speed: Optional[int] = None
    languages: Optional[List[str]] = None
    SpeciesTraits: Optional[List[Trait]] = None # List of traits specific to this species

# Traits specific to subspecies
class SubspeciesTraits(BaseModel):
    traits: List[Trait]  # List of traits specific to this subspecies

# Represents a variant of a species
class VariantTraits(BaseModel):
    traits: List[Trait]  # List of traits specific to this variant

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
    subspecies_traits: List[Trait]  # List of traits specific to this subspecies
    variants: Optional[List[Variant]] = []  # A list of variants, optional if none exist

# Main Species model representing a species and its subspecies
class Species(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    species_traits: SpeciesTraits  # Traits common to the species
    subspecies: Optional[List[Subspecies]] = []  # List of subspecies for this species