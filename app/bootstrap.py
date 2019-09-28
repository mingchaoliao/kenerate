import importlib
import inspect
import os
from typing import List, Dict


def command_lookup() -> Dict:
    cmd_dir = os.path.dirname(os.path.abspath(__file__)) + '/commands'
    cmd_files = list(filter(lambda f: f.endswith('.py'), os.listdir(cmd_dir)))
    cmd_file_names = list(map(lambda f: f[:-3], cmd_files))

    lookup = {}

    for f in cmd_file_names:
        module = importlib.import_module('app.commands.' + f)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != 'BaseCommand':
                lookup[obj.signature] = obj

    return lookup


def bootstrap(argv: List[str]):
    lookup = command_lookup()

    argc = len(argv)
    args = argv[2:]

    if argc < 2:
        return lookup['help'](list(lookup.values())).run()

    cmd = argv[1]
    if not lookup[cmd]:
        return lookup['help'](list(lookup.values())).run()

    return lookup[cmd](args).run()
