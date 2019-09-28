from typing import List

from app.base_command import BaseCommand


class Help(BaseCommand):
    signature = 'help'
    description = 'Displays help message'
    commands: List[BaseCommand] = []

    def __init__(self, commands: List[BaseCommand]):
        super().__init__([])
        self.commands = commands

    def handle(self) -> int:
        self.commands.sort(key=lambda c: c.signature)

        for cmd in self.commands:
            print('%-20s%s' % (cmd.signature, cmd.description))

        return 0
