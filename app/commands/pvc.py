from app.base_command import BaseCommand


class PersistentVolumeClaim(BaseCommand):
    signature = 'pvc'
    shortopts = 'l:s:c:n:h'
    longopts = [
        'rwo',
        'rom',
        'rwm',
        'help'
    ]
    description = 'Generate a template file for creating a PersistentVolumeClaim'

    def help(self) -> int:
        print(self.description)
        print()
        print('Usage:')
        print('kenerate pvc [flags] [options] <pvc_name>')
        print()
        print('Flags & Options:')
        print('%-20s%s' % ('-c', 'Specify "storageClassName"'))
        print('%-20s%s' % ('-l', 'Specify label query over volumes to consider for binding'))
        print('%-20s%s' % ('-n', 'Specify namespace that the pvc will be created in'))
        print('%-20s%s' % ('-h, --help', 'Display help message'))
        print('%-20s%s' % ('-s', 'Specify storage request. (e.g. 1Gi)'))
        print('%-20s%s' % ('--rwo', 'Use "ReadWriteOnce" in the "accessModes"'))
        print('%-20s%s' % ('--rom', 'Use "ReadOnlyMany" in the "accessModes"'))
        print('%-20s%s' % ('--rwm', 'Use "ReadWriteMany" in the "accessModes"'))

        return 0

    def handle(self) -> int:
        args = self.arguments()
        ops = self.options()

        if len(args) < 1:
            return self.fail('PersistentVolumeClaim name is required')

        pvc = {
            'apiVersion': 'v1',
            'kind': 'PersistentVolumeClaim',
            'metadata': {
                'name': args[0] + '-pvc'
            },
            'spec': {
                'accessModes': [],
                'resources': {
                    'requests': {
                        'storage': None
                    }
                },
                'selector': {
                    'matchLabels': {}
                }
            }
        }

        if '-c' in ops:
            pvc['spec']['storageClassName'] = ops['-c']

        if '-s' in ops:
            pvc['spec']['resources']['requests']['storage'] = ops['-s']

        if '-n' in ops:
            pvc['metadata']['namespace'] = ops['-n']

        if '-l' in ops:
            for label in ops['-l']:
                k, v = label.split('=')
                pvc['spec']['selector']['matchLabels'][k] = v

        access_modes = []

        if '--rwo' in ops:
            access_modes.append('ReadWriteOnce')

        if '--rom' in ops:
            access_modes.append('ReadOnlyMany')

        if '--rwm' in ops:
            access_modes.append('ReadWriteMany')

        pvc['spec']['accessModes'] = access_modes

        self.write_file(args[0] + '-pvc.yaml', pvc)

        return self.success()
