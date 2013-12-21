import os

from config import Config
from persistence import Persistence
from cronmanager import CronManager

CONFIG_FILE = '/etc/filereaper/filereaper.conf'


class FileReaper(object):

    modules_dir = None
    main_config_file = None

    def __init__(self, modules_dir, main_config_file=CONFIG_FILE):
        self.modules_dir = modules_dir
        self.main_config_file = main_config_file

    def run(self):
        main_config = Config(self.main_config_file)
        main_module = main_config.get_module()
        if not main_module:
            print "Error parsing main configuration file %s"\
                % self.main_config_file
            return False

        modules_configs = self._get_modules_configs(self.modules_dir)
        cron_manager = CronManager(main_module.executor,
                                   main_module.crons_path,
                                   main_module.crons_prefix)
        persistence = Persistence(main_module.persistence_file)

        # Identify new modules added
        new_modules = presistence.filter_old(modules_configs)
        old_modules = list(set(modules_configs) - set(new_modules))

        # Clean persistence by deleting the modules removed
        deleted_modules = persistence.clean(old_modules)

        # For those deleted from the persistence, remove the cron
        for module_config in deleted_modules:
            config = Config(module_config)
            module = config.get_module()
            if module:
                cron_manager.delete(module)

        # Add new modules to persistence and load their crons
        for module_config in new_modules:
            config = Config(module_config)
            module = config.get_module()
            if module:
                cron_manager.load(module)
                persistence.store(module)

    def _get_modules_configs(self, modules_dir):
        return map(lambda f: os.path.join(modules_dir, f),
                   os.listdir(modules_dir))
