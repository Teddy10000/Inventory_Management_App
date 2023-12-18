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
        