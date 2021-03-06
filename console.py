#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re


obj_class = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review
    }


class HBNBCommand(cmd.Cmd):
    """ The console """

    prompt = "(hbnb)"

    def do_quit(self, args):
        """
            Quit command to exit the program
        """

        return(True)

    def do_EOF(self, args):
        """
            EOF to exit the program
        """

        return(True)

    def emptyline(self):
        """
            An empty line executes anything
        """

        pass

    def do_create(self, args):
        """
            Creates a new instance of BaseModel,
            saves it (to the JSON file) and prints the id.
        """
        if not args:
            print("** class name missing **")
        elif not (args in obj_class):
            print("** class doesn't exist **")
        else:
            new = obj_class[args]()
            new.save()
            print(new.id)

    def default(self, args):
        """
            Recognize <class name>.all() and count instances
        """
        args_s = args.split('.')
        if len(args_s) == 2:
            if args_s[1] == "all()":
                self.do_all(args_s[0])
            elif args_s[1] == "count()":
                count = 0
                list_all = storage.all()
                for key, value in list_all.items():
                    token = str(key).split('.')
                    if args_s[0] == token[0]:
                        count += 1
                print(count)
            elif args_s[1][:4] == "show":
                id = re.split(r'show\("|"\)', args_s[1])
                string = args_s[0] + " " + id[1]
                self.do_show(string)
            elif args_s[1][:7] == "destroy":
                id = re.split(r'destroy\("|"\)', args_s[1])
                string = args_s[0] + " " + id[1]
                self.do_destroy(string)
            elif args_s[1][:6] == "update":
                pos = 0
                s_key = ""
                for i, s in enumerate(args_s[1], 0):
                    if s == '{':
                        pos = i
                        s_key = s
                        break
                if (s_key == '{'):
                    dic = args_s[1][(pos + 1):-2]
                    for line in dic.split(","):
                        value = line.split(":", 1)
                        print(value)
                        attr_1 = value[0].strip(" \"\'")
                        attr_2 = value[1].strip(" \"\'")
                        string = args_s[0] + " " + args_s[1][8:44] +\
                            " " + attr_1 + " " + attr_2
                        self.do_update(string)
                else:
                    list_u = re.split(r'update\("|"|, "|\)', args_s[1])
                    string = args_s[0] + " " + list_u[1] +\
                        " " + list_u[3] + " " + list_u[5]
                    self.do_update(string)

    def do_show(self, args):
        """
            Prints the string representation of an instance
        """

        if not args:
            print("** class name missing **")
        else:
            list_arg = args.split()
            if not list_arg[0] in obj_class:
                print("** class doesn't exist **")
            elif len(list_arg) == 1:
                print("** instance id missing **")
            else:
                dic_obj = storage.all()
                id_found = list_arg[0] + "." + list_arg[1]
                if id_found in dic_obj:
                    obj = dic_obj[id_found]
                    print(obj)
                else:
                    print("** no instance found **")

    def do_destroy(self, args):
        """
            Deletes an instance
        """

        if not args:
            print("** class name missing **")
        else:
            list_arg = args.split()
            if not list_arg[0] in obj_class:
                print("** class doesn't exist **")
            elif len(list_arg) == 1:
                print("** instance id missing **")
            else:
                dic_obj = storage.all()
                id_found = list_arg[0] + "." + list_arg[1]
                if id_found in dic_obj:
                    del dic_obj[id_found]
                    storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, args):
        """
            Prints all string representation of all instances.
        """
        list_all = []
        args_s = args.split(' ')
        if len(args) == 0:
            list_string = []
            for key, value in storage.all().items():
                list_all.append(str(value))
            print(list_all)
        elif args_s[0] not in obj_class:
            print("** class doesn't exist **")
        else:
            obj_all = storage.all()
            for key, value in obj_all.items():
                if args_s[0] == key.split('.')[0]:
                    list_all.append(str(value))
            print(list_all)

    def do_update(self, args):
        """
            Updates an instance
        """

        if not args:
            print("** class name missing **")
        else:
            list_arg = args.split(" ")
            if not list_arg[0] in obj_class:
                print("** class doesn't exist **")
            elif len(list_arg) == 1:
                print("** instance id missing **")
            else:
                dic_obj = storage.all()
                id_found = list_arg[0] + "." + list_arg[1]
                if id_found in dic_obj:
                    if len(list_arg) == 2:
                        print("** attribute name missing **")
                    elif len(list_arg) == 3:
                        print("** value missing **")
                    else:
                        obj = dic_obj[id_found]
                        setattr(obj, list_arg[2].replace('"', ''),
                                list_arg[3].replace('"', ''))
                        obj.save()
                else:
                    print("** no instance found **")

if __name__ == '__main__':
    console = HBNBCommand()
    console.cmdloop()
