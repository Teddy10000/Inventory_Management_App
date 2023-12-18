#!/usr/bin/python 3

"""Module for FileStorage class"""

import datetime
import json
import os

class FileStorage:
    """Class for storing the orders data"""
    __file_path = "file.json" 
    __objects = {}

    def all(self):
        """The all method returns everything """
        return FileStorage.__objects
    
    def new(self,obj):
        """TAKES IN THE OBJECTS TO CREATE A DICTIONARY WITH KEY AND SAVE TO THE __OBJECTS"""
        key = "{}.{}".format(type(obj).__name__,obj.id) 
        ## assign the object to the key to store in __objects
        FileStorage.__objects[key] = obj

    def save(self):
        with open(FileStorage.__file_path, "w",encoding='utf-8') as f:
            """Dictionary comprehension that creates a dictionary data with by convertin the values to dictionatu"""
            data = {k : v.to_dict() for k,v in FileStorage.__objects.items()}
            json.dump(data, f)

    def classes(self):
        from models import Ingredients,MenuItem,Supplier,Order,OrderItem

        classes = {
            "Ingredients": Ingredients ,
            "MenuItem":MenuItem,
            "Supplier":Supplier,
            "Order":Order,
            "OrderItem":OrderItem
        }
        return classes
        

    def reload(self):
        """Just fetch from the file """

        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r",encoding="utf8") as f:
            obj_dict = json.load(f) 
            obj_dict = {k:self.classes()[v["__class__"]] for k,v in obj_dict.items()}
            #OVERWRITING THE ENTIRE FILESTORAGE
            FileStorage.__objects = obj_dict
