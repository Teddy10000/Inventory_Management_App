#!/usr/bin/python 3

"""Module for FileStorage class"""

import datetime
import json
import os
from tabulate import tabulate

class FileStorage:
    """Class for storing the orders data"""
    __file_path = "file.json" 
    __objects = {}

    def all(self):
        """The all method returns everything"""
        objects = FileStorage.__objects.values()
        headers = ["Class", "ID", "Created At", "Updated At", "Attributes"]

        formatted_objects = []
        for obj in objects:
            class_name = type(obj).__name__
            obj_id = obj.id
            created_at = obj.created_at
            updated_at = obj.updated_at
            attributes = obj.to_dict()
            formatted_objects.append([class_name, obj_id, created_at, updated_at, attributes])

        return tabulate(formatted_objects, headers=headers)
    
    def new(self,obj):
        """TAKES IN THE OBJECTS TO CREATE A DICTIONARY WITH KEY AND SAVE TO THE __OBJECTS"""
        key = "{}.{}".format(type(obj).__name__,obj.id) 
        ## assign the object to the key to store in __objects
        FileStorage.__objects[key] = obj

    def update_ingredient_qunatity(self,ingredient_name,quantity):
        from ..models import Ingredients, MenuItem,Supplier,Order,OrderItem
        """Update a quantity of an ingredient after creation of the ingredient"""
        for obj in self.__objects.values():
            if isinstance(obj,Ingredients) and obj.name == ingredient_name:
                obj.quantity -= quantity
                self.save()
                return
            
    def ingredient_exists(self, ingredient_name):
        from ..models import Ingredients
        """Check if an ingredient with a specific name exists"""
        for obj in self.__objects.values():
            if isinstance(obj, Ingredients) and obj.name == ingredient_name:
                return True
        return False
    
    def create_menu_item(self,name,ingredients_data,price):
        from ..models import Ingredients,MenuItem
                # Check if all ingredients exist before creating MenuItem
        for ingredient_name, quantity in ingredients_data:
            if not self.ingredient_exists(ingredient_name):
                print(f"Ingredient '{ingredient_name}' doesn't exist. Cannot create MenuItem.")
                return

        # All ingredients exist, create MenuItem and update quantities
        new_menu_item = MenuItem(name=name, ingredients=ingredients_data, price=price)
        self.new(new_menu_item)
        self.save()

        # Update ingredient quantities
        for ingredient_name, quantity in ingredients_data:
            self.update_ingredient_quantity(ingredient_name, quantity)

        print(f"MenuItem '{name}' created with ingredients {ingredients_data}.")


    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        """Calling the objects"""
        odict = FileStorage.__objects
        """changing to dictionary"""
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def classes(self):
       
        from ..models import Ingredients, MenuItem,Supplier,Order,OrderItem
        classes = {
            "Ingredients": Ingredients,
            "MenuItem":MenuItem,
            "Supplier":Supplier,
            "Order":Order,
            "OrderItem":OrderItem
        }
        return classes
        

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        from ..models import Ingredients, MenuItem,Supplier,Order,OrderItem
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
