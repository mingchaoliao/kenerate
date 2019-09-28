from app.base_command import BaseCommand


class Version(BaseCommand):
    signature = 'version'
    description = 'Print the tool version information'

    def handle(self) -> int:
        print('Version: 0.1.0')

        return 0
