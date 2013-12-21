from ConfigParser import ConfigParser, MissingSectionHeaderError, ParsingError

from filereaper_module import FileReaperModule


class Config(object):

    config_file = None
    module = None

    def __init__(self, config_file):
        self.config_file = config_file

    def get_module(self):
        config = ConfigParser()
        try:
            success = config.read(self.config_file)
        except MissingSectionHeaderError:
            print "Error parsing config file %s, there is no section header"\
                % self.config_file
            return None
        except ParsingError as e:
            print "Error parsing config file %s: %s" % (self.config_file, e)
            return None
        if not success:
            print "Config file %s does not exist" % self.config_file
            return None
        section = config.sections()[0]
        self.module = FileReaperModule(section, config.items(section))
        return self.module
