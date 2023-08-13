#!/usr/bin/python3
""" Entry point of the command interpreter """

import cmd
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.user import User
from models.place import Place
import shlex
import json

class HBNBCommand(cmd.Cmd):
    """Simple command processor example."""
    prompt = "(hbnb) "
    func_list = ['create', 'show', 'update', 'all', 'destroy', 'count']
    classes_list = ['BaseModel', 'User', 'Amenity',
                 'Place', 'City', 'State', 'Review']

    def precmd(self, arg):
        """parses command input"""
        if '.' in arg and '(' in arg and ')' in arg:
            cls = arg.split('.')
            cnd = cls[1].split('(')
            args = cnd[1].split(')')
            clHb = HBNBCommand.classes_list
            funcHb = HBNBCommand.func_list
            if cls[0] in clHb and cnd[0] in funcHb:
                arg = cnd[0] + ' ' + cls[0] + ' ' + args[0]
        return arg

    def help_help(self):
        """ Prints help command description """
        print("Provides description of a given command")

    def emptyline(self):
        """do nothing when empty line"""
        pass

    def do_count(self, cls_name):
        """counts number of instances of a class"""
        count = 0
        objects_all = storage.all()
        for k, v in objects_all.items():
            clss = k.split('.')
            if clss[0] == cls_name:
                count = count + 1
        print(count)

    def do_create(self, type_model):
        """ Creates an instance according to a given class """

        if not type_model:
            print("** class name missing **")
        elif type_model not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        else:
            dct = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
                   'City': City, 'Amenity': Amenity, 'State': State,
                   'Review': Review}
            my_model = dct[type_model]()
            print(my_model.id)
            my_model.save()

    def do_show(self, arg):
        """ Shows string representation of an instance passed """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objects_all = storage.all()
            for k, v in objects_all.items():
                nmObj = v.__class__.__name__
                idObj = v.id
                if nmObj == args[0] and idObj == args[1].strip('"'):
                    print(v)
                    return
            print("** no instance found **")

    def do_destroy(self, arg):
        """ Deletes an instance passed """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objects_all = storage.all()
            for k, v in objects_all.items():
                nmObj = v.__class__.__name__
                idObj = v.id
                if nmObj == args[0] and idObj == args[1].strip('"'):
                    del v
                    del storage._FileStorage__objects[k]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """ Prints string represention of all instances of a given class """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        else:
            lsInstan = []
            objects_all = storage.all()
            for k, v in objects_all.items():
                nmObj = v.__class__.__name__
                if nmObj == args[0]:
                    lsInstan += [v.__str__()]
            print(lsInstan)

    def do_update(self, arg):
        """ Updates an instance based on the class name and id """

        if not arg:
            print("** class name missing **")
            return

        a = ""
        for argv in arg.split(','):
            a = a + argv

        args = shlex.split(a)

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objects_all = storage.all()
            for k, objc in objects_all.items():
                nmObj = objc.__class__.__name__
                idObj = objc.id
                if nmObj == args[0] and idObj == args[1].strip('"'):
                    if len(args) == 2:
                        print("** attribute name missing **")
                    elif len(args) == 3:
                        print("** v missing **")
                    else:
                        setattr(objc, args[2], args[3])
                        storage.save()
                    return
            print("** no instance found **")

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """ function to exit the command interpreter """
        return True
    
if __name__ == '__main__':
    HBNBCommand().cmdloop()
