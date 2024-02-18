def do_create(self, arg):
    """Create a new instance of a class"""
    if not arg:
        print("** class name missing **")
        return

    args = arg.split()
    class_name = args[0]
    if class_name not in HBNBCommand.classes:
        print("** class doesn't exist **")
        return

    param_dict = {}
    for param in args[1:]:
        if "=" not in param:
            continue
        key, value = param.split("=")
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ')
        elif '.' in value:
            try:
                value = float(value)
            except ValueError:
                continue
        else:
            try:
                value = int(value)
            except ValueError:
                continue
        param_dict[key] = value

    new_instance = HBNBCommand.classes[class_name](**param_dict)
    new_instance.save()
    print(new_instance.id)
