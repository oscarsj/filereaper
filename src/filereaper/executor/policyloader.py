import importlib


class PolicyLoader(object):

    BASE_MODULES = 'filereaper.executor.policies'

    def load(self, name, value, params=None):
        class_name = name.title().replace('_', '')
        file_name = name
        #TODO this is not compatible with 2.6
        if self.BASE_MODULES:
            module_name = "%s.%s" % (self.BASE_MODULES, file_name)
        else:
            module_name = file_name

        try:
            mod = importlib.import_module(module_name)
            return getattr(mod, class_name)(value, params)
        except ImportError as e:
            print "Error loading policy %s, the file does not exists" % name
            print e
            return None
        except AttributeError as e:
            print """The file %s does not contain a valid class name,
                     it must be: %s""" % (file_name, class_name)
            print e
            return None
        except TypeError as e:
            print """The policy %s could be loaded but the constructor is
                     invalid""" % name
            print e
            return None
