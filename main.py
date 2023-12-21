import cmd
import re
from shlex import split 
from app.models import BaseModel,storage,Supplier,Ingredients,MenuItem,Order,OrderItem 



def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl 
    

class InventoryMCommand(cmd.Cmd):
    """Defines all the command for my restaurant management app"""

    prompt = "(Aisha's Kitchen)"
    __classes = {
        "BaseModel",
        "Ingredients",
        "Supplier",
        "MenuItem",
        "Order",
        "OrderItem"
    }
    

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "help-create":self.help_create
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class> [<attribute_name>="<attribute_value>" ...]
        Create a new class instance and print its id."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in InventoryMCommand.__classes:
            print("** class doesn't exist **")
        else:
            class_name = argl[0]
            new_instance = eval(class_name)()  # Create instance of specified class

            # Set attributes for the instance
            provided_attributes = argl[1:]
            expected_attributes = [attr for attr in dir(new_instance) if not attr.startswith('_') and attr not in ['id', 'created_at', 'save', 'updated_at', 'to_dict']] # Get the class attributes
            print(expected_attributes)
            if class_name == "MenuItem":
                attributes = dict(attribute.split('=') for attribute in provided_attributes)
                
                if 'ingredients' in attributes:
                    # Extract and format ingredient data
                    ingredients_data = []
                    ingredients_info = attributes['ingredients'].split(';')
                    for ingredient_info in ingredients_info:
                        ingredient_name, quantity = ingredient_info.split('=')
                        ingredients_data.append((ingredient_name, int(quantity)))

                    # Create a new MenuItem and update ingredient quantities
                    storage.create_menu_item(attributes.get('name', ''), ingredients_data, int(attributes.get('price', 0)))
                    return

            # Set attributes for other classes
            for attribute in provided_attributes:
                attr_split = attribute.split('=')
                if len(attr_split) != 2:
                    print(f"Attribute '{attribute}' is not in the format 'name=value'. Skipping.")
                    continue

                attr_name, attr_value = attr_split
                setattr(new_instance, attr_name, attr_value)

            # Check if provided attributes match expected attributes
            provided_attr_set = set(attr.split('=')[0] for attr in provided_attributes) 

            expected_attr_set = set(expected_attributes)

            if provided_attr_set != expected_attr_set:
                print(f"** Provided attributes do not match the model attributes. Aborting save. expected {expected_attributes} but gave only {provided_attr_set} **")
            else:
                # Save the instance and print its ID
                storage.new(new_instance)
                storage.save()
                print(new_instance.id)

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in InventoryMCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in InventoryMCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
                """Usage: all or all <class> or <class>.all()
                Display string representations of all instances of a given class.
                If no class is specified, displays all instantiated objects."""
                argl = parse(arg)
                if len(argl) > 0 and argl[0] not in InventoryMCommand.__classes:
                    print("** class doesn't exist **")
                else:
                    output = storage.all()
                    print(output)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def help_create(self):
        print("Create a new instance of a class.")
        print("Usage: create <class> [<attribute_name>='<attribute_value>' ...]")
        print("Supported classes:")
        for cls_name in InventoryMCommand.__classes:
            print(f"- {cls_name}")
        print("Example:")
        print("create Ingredients name='Flour' quantity=5 unit='kg'")
        print("create MenuItem name='Dish' price=10.5")
        # Add more examples for other classes

# Add similar methods for other commands (e.g., do_update, do_show, etc.) with appropriate usage and examples.
# These methods should handle updating attributes and provide help

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) < 4:
            print("** insufficient arguments provided for update command **")
            return False

        class_name = argl[0]
        instance_id = argl[1]
        attribute_name = argl[2]

        # Check if the provided class name exists in the available classes
        if class_name not in InventoryMCommand.__classes:
            print("** class doesn't exist **")
            return False

        # Check if the instance exists in the object dictionary
        instance_key = "{}.{}".format(class_name, instance_id)
        if instance_key not in objdict:
            print("** no instance found **")
            return False

        # Update the attribute of the instance
        new_value = argl[3]
        obj = objdict[instance_key]
        setattr(obj, attribute_name, new_value)

        storage.save()
        return True



if __name__ == "__main__":
    InventoryMCommand().cmdloop()