from app.base_command import BaseCommand


class Namespace(BaseCommand):
    signature = 'ns'
    shortopts = 'h'
    longopts = [
        'help'
    ]
    description = 'Generate a template file for creating a namespace'

    def help(self) -> int:
        print(self.description)
        print()
        print('Usage:')
        print('kenerate ns [flags] [options] <ns_name>')
        print()
        print('Flags & Options:')
        print('%-20s%s' % ('-h, --help', 'Display help message'))

        return 0

    def handle(self) -> int:
        args = self.arguments()

        if len(args) < 1:
            return self.fail('Namespace name is required')

        ns = {
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {
                'name': args[0] + '-ns'
            },
            'spec': {}
        }

        self.write_file(args[0] + '-ns.yaml', ns)

        return self.success()
