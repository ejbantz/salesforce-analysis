import os
import xml.etree.ElementTree as ET

# Constants
XML_NAMESPACE = "{http://soap.sforce.com/2006/04/metadata}"
OBJECTS_DIR = "force-app/main/default/objects"

def extract_relationships_with_field_name(object_folder):
    """
    Extract relationships along with the field name from the fields of a given object.
    """
    relationships = []
    
    # Path to the fields folder for the object
    fields_folder = os.path.join(object_folder, "fields")
    
    # Check if the fields folder exists for the object
    if os.path.exists(fields_folder):
        for field_file in os.listdir(fields_folder):
            # Parse the XML file for the field
            tree = ET.parse(os.path.join(fields_folder, field_file))
            root = tree.getroot()
            
            # Extract field type and referenced object considering the namespace
            field_type = root.find(f"{XML_NAMESPACE}type").text if root.find(f"{XML_NAMESPACE}type") is not None else None
            reference_to_elements = root.findall(f"{XML_NAMESPACE}referenceTo")
            
            # If the field type is Lookup or MasterDetail, capture the relationship
            if field_type in ["Lookup", "MasterDetail"]:
                field_name = field_file.replace(".field-meta.xml", "")
                if reference_to_elements:
                    for ref in reference_to_elements:
                        if ref.text:
                            relationships.append((field_type, ref.text, field_name))
                # Fallback: If no referenceTo node is found, derive object name from field name
                elif field_file.endswith("Id.field-meta.xml"):
                    related_object_name = field_file.replace("Id.field-meta.xml", "")
                    relationships.append((field_type, related_object_name, field_name))
                
    return relationships

def generate_final_plantuml(object_relationships):
    """
    Generate the final PlantUML representation including field names.
    """
    uml_list = ["@startuml"]
    
    # Define classes for each object
    for obj in object_relationships.keys():
        uml_list.append(f"class {obj} {{\n}}")
    
    # Define relationships
    for obj, relationships in object_relationships.items():
        for rel in relationships:
            field_type, reference_to, field_name = rel
            if field_type == "Lookup":
                uml_list.append(f"{obj} --> {reference_to} : {field_name}")
            elif field_type == "MasterDetail":
                uml_list.append(f"{obj} *-- {reference_to} : {field_name}")
    
    uml_list.append("@enduml")
    
    return "\n".join(uml_list)

# Extract relationships for all objects
object_relationships_with_field_name = {}
for obj in os.listdir(OBJECTS_DIR):
    obj_path = os.path.join(OBJECTS_DIR, obj)
    if os.path.isdir(obj_path):  # Ensure it's a directory
        object_relationships_with_field_name[obj] = extract_relationships_with_field_name(obj_path)

# Generate the final PlantUML code
final_plantuml_code = generate_final_plantuml(object_relationships_with_field_name)
print(final_plantuml_code)

