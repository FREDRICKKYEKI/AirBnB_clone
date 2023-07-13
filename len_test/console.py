#!/usr/bin/python3
"""
This is the entry point for the command interpreter
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Runs a command line interpreter for our program
    """

    prompt = '(hbnb) '
    class_list = ["BaseModel", "User", "State", "City",
                  "Amenity", "Place", "Review"]

    def do_create(self, args):
        """Creates a new instance of the BaseModel class
        Saves it and prints the id of the instance
        Usage: create <class name>"""
        list_args = args.split()
        if args == "":
            print("** class name missing **")
        elif list_args[0] in self.class_list:
            new = eval(list_args[0])()
            print(new.id)
            new.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of a class instance
        based on class name and id
        Usage: show <class name> <id>"""
        list_args = args.split()
        if args == "":
            print("** class name missing **")
        elif list_args[0] not in self.class_list:
            print("** class doesn't exist **")
        elif len(list_args) < 2:
            print("** instance id missing **")
        else:
            all_obj = storage.all()  # get all objects from storage
            name_id = "{}.{}".format(list_args[0], list_args[1])
            # check if key is present in dictionary
            if name_id in all_obj.keys():
                print(all_obj[name_id])
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance given the class name and id and saves changes
        Usage: destroy <class name> <id>"""
        list_args = args.split()
        if args == "":
            print("** class name missing **")
        elif list_args[0] not in self.class_list:
            print("** class doesn't exist **")
        elif len(list_args) < 2:
            print("** instance id missing **")
        else:
            all_obj = storage.all()  # get all objects from storage
            name_id = "{}.{}".format(list_args[0], list_args[1])

            # check if key is present in dictionary
            if name_id in all_obj.keys():
                del all_obj[name_id]
                storage.save()
            else:  # if key is not present
                print("** no instance found **")

    def do_all(self, args):
        """Prints all string representation based on class name or not
        Usage: all <optional: class name>"""
        list_args = args.split()
        all_obj = storage.all()  # get all objects from storage
        if args == "":  # if no arguments provided
            print_list = []
            for key, value in all_obj.items():
                print_list.append(str(value))
            print(print_list)

        else:  # if there is an argument
            if list_args[0] in self.class_list:  # if class exists
                print_list = []
                for key, value in all_obj.items():
                    if value.__class__.__name__ == list_args[0]:
                        print_list.append(str(value))
                print(print_list)
            else:
                print("** class doesn't exist **")

    def do_update(self, args):
        """Updates an instance based on the class name and id
        Usage: update <class name> <id> <attribute name> '<attribute value>'"""
        list_args = args.split()
        all_obj = storage.all()  # get all objects from storage
        if args == "":  # if no arguments provided
            print("** class name missing **")

        elif list_args[0] not in self.class_list:  # class does not exist
            print("** class doesn't exist **")

        elif len(list_args) < 2:   # id parameter not provided
            print("** instance id missing **")

        else:
            # get key value representation from the class name and id
            name_id = "{}.{}".format(list_args[0], list_args[1])

            if name_id in all_obj.keys():
                if len(list_args) < 3:  # no attribute argument given
                    print("** attribute name missing **")

                elif len(list_args) < 4:  # attribute value not given
                    print("** value missing **")

                else:
                    obj_dict = all_obj[name_id].__dict__
                    if list_args[2] in obj_dict.keys():
                        # maintain the type if present
                        obj_dict[list_args[2]] = type(obj_dict[list_args[2]]
                                                      )(list_args[3])
                    else:
                        obj_dict[list_args[2]] = list_args[3]  # create new

                    storage.save()

            else:  # instance with the given id not found
                print("** no instance found **")

    def do_quit(self, line):
        """Quit command to exit the program"""
        return (True)

    def do_EOF(self, line):
        """EOF command to exit the program"""
        return (True)

    def emptyline(self):
        """an empty line + ENTER key does nothing"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
