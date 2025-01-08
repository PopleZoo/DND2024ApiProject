import os

from fastapi import FastAPI, HTTPException
import json
import logging
from models import Species, Subspecies, Traits
from typing import List
import csv

# Initialize FastAPI application
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to validate JSON data
def validate_data(data, required_keys):
    for entry in data:
        for key in required_keys:
            if key not in entry:
                raise ValueError(f"Missing key '{key}' in entry: {entry}")

# Function to load classes from a JSON file
def load_classes_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Log the structure of the loaded data
            logger.info(f"Loaded classes data structure: {type(data)}")

            # Check if the data is a dictionary and contains 'classes'
            if isinstance(data, dict) and 'classes' in data:
                classes_data = data['classes']  # Access the list inside the dictionary
            else:
                raise ValueError(f"Expected a dictionary with a 'classes' key, but got {type(data)} instead.")

            # Process each class entry
            for class_entry in classes_data:
                if 'definition' in class_entry:
                    class_entry['description'] = class_entry['definition'].get('description', '')
                    class_entry.update(class_entry.pop('definition', {}))  # Merge 'definition' into the class_entry

                # Ensure subclasses are also loaded
                if 'subclasses' in class_entry:
                    for subclass in class_entry['subclasses']:
                        for feature in subclass.get('features', []):
                            feature['level'] = feature.get('level', 0)  # Ensure level is set

            return classes_data
    except Exception as e:
        logger.error(f"Error loading classes from {file_path}: {e}")
        return []

# Function to load species from a JSON file
def load_species_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Directly return parsed JSON without converting to custom objects
        return data.get("species", [])
    except Exception as e:
        logger.error(f"Error loading species from {file_path}: {e}")
        return []



# Function to load items from the CSV file
def load_items_from_csv(file_path):
    try:
        items = []
        with open(file_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                items.append({
                    "category": row["Category"],
                    "subCategory": row["Sub-Category"],
                    "item": row["Item"],
                    "weight": row["Weight"],
                    "cost": row["Cost"],
                    "source": row["Source"],
                    "shops": {
                        "generalStore": row["General Store"],
                        "adventuring": row["Adventuring"],
                        "tailor": row["Tailor"],
                        "jeweler": row["Jeweler"],
                    }
                })
        return items
    except Exception as e:
        logger.error(f"Error loading items from {file_path}: {e}")
        return []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the classes, species, and items when the app starts
classes = load_classes_from_json(os.path.join(BASE_DIR, "classes.json"))
species = load_classes_from_json(os.path.join(BASE_DIR, "species.json"))
items = load_items_from_csv("D&D5E2024_Stores_V1.0 - Master.csv")

# Endpoint to fetch all classes, including subclasses and features
@app.get("/api/classes", response_model=list)
async def get_all_classes():
    logger.info("Fetching all classes")
    return classes

# Endpoint to fetch a specific class, including subclasses and features
@app.get("/api/classes/{class_id}", response_model=dict)
async def get_class(class_id: str):
    logger.info(f"Fetching class with ID: {class_id}")
    clazz = next((c for c in classes if c["id"] == class_id), None)
    if not clazz:
        logger.warning(f"Class not found: {class_id}")
        raise HTTPException(status_code=404, detail="Class not found")
    return clazz

# Updated endpoint to fetch subclass by class_id and subclass_id
@app.get("/api/classes/{class_id}/subclasses/{subclass_id}", response_model=dict)
async def get_subclass_from_class(class_id: str, subclass_id: str):
    try:
        # Ensure that classes is a list of dictionaries
        if not isinstance(classes, list):
            logger.error(f"Expected classes to be a list, got {type(classes)}")
            raise HTTPException(status_code=500, detail="Internal server error")

        # Find the class by its ID
        clazz = next((c for c in classes if c["id"] == class_id), None)
        if not clazz:
            logger.warning(f"Class not found: {class_id}")
            raise HTTPException(status_code=404, detail="Class not found")

        # Find the subclass within the class
        subclass = next((s for s in clazz.get("subclasses", []) if s["id"] == subclass_id), None)
        if not subclass:
            logger.warning(f"Subclass not found: {subclass_id}")
            raise HTTPException(status_code=404, detail="Subclass not found")

        return subclass

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoint to fetch all species
@app.get("/api/species", response_model=List[Species])
async def get_all_species():
    logger.info("Fetching all species")
    return species

# Endpoint to fetch a specific species by its ID
@app.get("/api/species/{species_id}", response_model=dict)
async def get_species(species_id: str):
    logger.info(f"Fetching species with ID: {species_id}")
    specie = next((s for s in species if s["id"] == species_id), None)
    if not specie:
        logger.warning(f"Species not found: {species_id}")
        raise HTTPException(status_code=404, detail="Species not found")
    return specie

# Endpoint to fetch a specific subspecies by species_id and subspecies_id
@app.get("/api/species/{species_id}/subspecies/{subspecies_id}", response_model=dict)
async def get_subspecies(species_id: str, subspecies_id: str):
    specie = next((s for s in species if s["id"] == species_id), None)
    if not specie:
        logger.warning(f"Species not found: {species_id}")
        raise HTTPException(status_code=404, detail="Species not found")

    subspecies = next((ss for ss in specie.get("subspecies", []) if ss["id"] == subspecies_id), None)
    if not subspecies:
        logger.warning(f"Subspecies not found: {subspecies_id}")
        raise HTTPException(status_code=404, detail="Subspecies not found")

    return subspecies

# Endpoint to fetch a specific variant by species_id, subspecies_id, and variant_id
@app.get("/api/species/{species_id}/subspecies/{subspecies_id}/variants/{variant_id}", response_model=dict)
async def get_variant(species_id: str, subspecies_id: str, variant_id: str):
    specie = next((s for s in species if s["id"] == species_id), None)
    if not specie:
        logger.warning(f"Species not found: {species_id}")
        raise HTTPException(status_code=404, detail="Species not found")

    subspecies = next((ss for ss in specie.get("subspecies", []) if ss["id"] == subspecies_id), None)
    if not subspecies:
        logger.warning(f"Subspecies not found: {subspecies_id}")
        raise HTTPException(status_code=404, detail="Subspecies not found")

    variant = next((v for v in subspecies.get("variants", []) if v["id"] == variant_id), None)
    if not variant:
        logger.warning(f"Variant not found: {variant_id}")
        raise HTTPException(status_code=404, detail="Variant not found")

    return variant

# Endpoint to fetch all variants for a specific subspecies
@app.get("/api/species/{species_id}/subspecies/{subspecies_id}/variants", response_model=List[dict])
async def get_variants(species_id: str, subspecies_id: str):
    try:
        # Find the species
        specie = next((s for s in species if s.id == species_id), None)
        if not specie:
            logger.warning(f"Species not found: {species_id}")
            raise HTTPException(status_code=404, detail="Species not found")

        # Find the subspecies
        subspecies = next((ss for ss in specie.subspecies if ss.id == subspecies_id), None)
        if not subspecies:
            logger.warning(f"Subspecies not found: {subspecies_id}")
            raise HTTPException(status_code=404, detail="Subspecies not found")

        return subspecies.variants

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to fetch all items
@app.get("/api/items", response_model=List[dict])
async def get_all_items():
    logger.info("Fetching all items")
    return items

# Endpoint to fetch specific item
@app.get("/api/items/{item_name}", response_model=dict)
async def get_item(item_name: str):
    logger.info(f"Fetching item: {item_name}")
    item = next((i for i in items if i["item"].lower() == item_name.lower()), None)
    if not item:
        logger.warning(f"Item not found: {item_name}")
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Endpoint to fetch items of a specific category
@app.get("/api/items/category/{category_name}", response_model=List[dict])
async def get_items_by_category(category_name: str):
    category_items = [i for i in items if i["category"].lower() == category_name.lower()]
    if not category_items:
        raise HTTPException(status_code=404, detail="No items found in this category")
    return category_items

# Endpoint to fetch items of a specific subcategory
@app.get("/api/items/subcategory/{sub_category_name}", response_model=List[dict])
async def get_items_by_subcategory(sub_category_name: str):
    sub_category_items = [i for i in items if i["subCategory"].lower() == sub_category_name.lower()]
    if not sub_category_items:
        raise HTTPException(status_code=404, detail="No items found in this subcategory")
    return sub_category_items

# Endpoint to fetch items available at a specific shop
@app.get("/api/items/shop/{shop_name}", response_model=List[dict])
async def get_items_by_shop(shop_name: str):
    valid_shops = ["generalStore", "adventuring", "tailor", "jeweler"]
    if shop_name not in valid_shops:
        raise HTTPException(status_code=400, detail="Invalid shop name")

    shop_items = [i for i in items if i["shops"].get(shop_name, False)]
    if not shop_items:
        raise HTTPException(status_code=404, detail=f"No items found in {shop_name.replace('_', ' ').title()}")
    return shop_items