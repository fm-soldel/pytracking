import importlib
import os

class EnvSettings:
    def __init__(self):
        self.results_path = 'tracking_results/'
        self.network_path = '../networks/'
        self.otb_path = ''
        self.nfs_path = ''
        self.uav_path = ''
        self.tpl_path = ''
        self.vot_path = ''
        self.got10k_path = ''
        self.lasot_path = ''
        self.trackingnet_path = ''


def env_settings():
    env_module_name = 'pytracking.evaluation.local'
    try:
        env_module = importlib.import_module(env_module_name)
        return env_module.local_env_settings()
    except:
        env_file = os.path.join(os.path.dirname(__file__), 'local.py')

        comment = {'results_path': 'Where to store tracking results',
                   'network_path': 'Where tracking networks are stored.'}

        with open(env_file, 'w') as f:
            settings = EnvSettings()

            f.write('from pytracking.evaluation.environment import EnvSettings\n\n')
            f.write('def local_env_settings():\n')
            f.write('    settings = EnvSettings()\n\n')
            f.write('    # Set your local paths here.\n\n')

            for attr in dir(settings):
                comment_str = None
                if attr in comment:
                    comment_str = comment[attr]
                attr_val = getattr(settings, attr)
                if not attr.startswith('__') and not callable(attr_val):
                    if comment_str is None:
                        f.write('    settings.{} = \'{}\'\n'.format(attr, attr_val))
                    else:
                        f.write('    settings.{} = \'{}\'    # {}\n'.format(attr, attr_val, comment_str))
            f.write('\n    return settings\n\n')

            raise RuntimeError('YOU HAVE NOT SETUP YOUR local.py!!!\n Go to "{}" and set all the paths you need. Then try to run again.'.format(env_file))
