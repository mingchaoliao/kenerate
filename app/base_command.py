from getopt import gnu_getopt
from typing import List, Dict

import yaml


class BaseCommand:
    signature: str = None
    description: str = ''
    shortopts: str = ''
    longopts: List[str] = []
    argv: List[str] = []

    def __init__(self, argv: List[str]):
        self.argv = argv

    def arguments(self) -> List[str]:
        ops, args = gnu_getopt(self.argv, self.shortopts, self.longopts)
        return args

    def options(self) -> Dict:
        ops, args = gnu_getopt(self.argv, self.shortopts, self.longopts)
        res = {}

        for k, v in ops:
            if k in res:
                if not isinstance(res[k], list):
                    res[k] = [res[k]]
                res[k].append(v)
            else:
                res[k] = v

        return res

    def read_yaml_file(self, path: str):
        with open(path, 'r') as file:
            return yaml.load(file, yaml.Loader)

    def write_file(self, path: str, content: Dict):
        with open(path, 'w') as file:
            file.write(yaml.dump(content))

    def success(self, msg: str = ''):
        if len(msg) > 0:
            print('Successs: ' + msg)
        return 0

    def fail(self, msg: str = ''):
        if len(msg) > 0:
            print('Error: ' + msg)
        return 1

    def run(self) -> int:
        ops = self.options()

        if '-h' in ops or '--help' in ops:
            return self.help()

        return self.handle()

    def help(self) -> int:
        return 0

    def handle(self) -> int:
        return 0
