from app.base_command import BaseCommand


class Pod(BaseCommand):
    signature = 'pod'
    shortopts = 'hl:n:'
    longopts = [
        'help'
    ]
    description = 'Generate a template file for creating a pod'

    def help(self) -> int:
        print(self.description)
        print()
        print('Usage:')
        print('kenerate pod [flags] [options] <ns_name>')
        print()
        print('Flags & Options:')
        print('%-20s%s' % ('-h, --help', 'Display help message'))
        print('%-20s%s' % ('-l', 'Specify labels associate with the pod'))
        print('%-20s%s' % ('-n', 'Specify namespace that the pod will be created in'))

        return 0

    def handle(self) -> int:
        args = self.arguments()
        ops = self.options()

        if len(args) < 1:
            return self.fail('Pod name is required')

        pod = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': args[0] + '-pod',
            },
            'spec': {
                'containers': [
                    {
                        'name': 'redis',
                        'image': 'redis'
                    }
                ]
            }
        }

        if '-n' in ops:
            pod['metadata']['namespace'] = ops['-n']

        labels = {}
        if '-l' in ops:
            for label in ops['-l']:
                k, v = label.split('=')
                labels[k] = v
            pod['metadata']['labels'] = labels

        self.write_file(args[0] + '-pod.yaml', pod)

        return self.success()
