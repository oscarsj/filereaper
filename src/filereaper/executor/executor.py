import os
import re
import copy

import policyloader
import context
import file_object
import params_config


class Executor(object):
    params = None
    test_mode = None

    def __init__(self, params):
        self.base_params_list = params_config.BASE_PARAMS
        self.policy_params_list = params_config.POLICIES
        self.params = params
        self.test_mode = params['test_mode']\
            if params and 'test_mode' in params else True

    def execute(self):
        base_params = self._extract_base_params(self.params)
        files_to_remove = self._build_files_to_remove(base_params)
        self._perform_removal(files_to_remove, base_params['path'])

    def _build_files_to_remove(self, base_params):
        """
        Build the files to remove list applying the given policies using
        a strategy pattern
        """
        file_match = base_params['file_match']
        path = base_params['path']
        all_files_sorted = self._get_all_files_sorted(
            path, file_match, base_params['time_mode'],
            base_params['recurse'], base_params['remove_links'])
        files_to_remove = all_files_sorted
        ploader = policyloader.PolicyLoader()

        # Setting keepminimum first, as it's the higher priority
        if 'keepminimum' in base_params and base_params['keepminimum'] > 0:
                self.policy_params_list.insert(0, 'keepminimum')
                self.params.update({'keepminimum': base_params['keepminimum']})

        # Applying policies
        for param in self.policy_params_list:
            if param in self.params and self.params[param]:
                policy = ploader.load(param, self.params[param],
                                      base_params)
                policy.set_files(all_files_sorted)
                cntx = context.Context(policy)
                from_policy = cntx.execute_policy()
                files_to_remove = self._lists_intersection(files_to_remove,
                                                           from_policy)

        # Excluding files specified in params
        if 'exclude_list' in base_params and base_params['exclude_list']:
            to_exclude = filter(None, base_params['exclude_list'].split(','))
            to_exclude_abs = map(lambda f: os.path.join(path, f),
                                 to_exclude)
            files_to_remove = self._exclude_files(files_to_remove,
                                                  to_exclude_abs)
        return files_to_remove

    def _exclude_files(self, files, to_exclude):
        # This must preserve the order, cannot use set()
        #TODO improve this
        for f in to_exclude:
            files.remove(file_object.FileObject(f))
        return files

    def _extract_base_params(self, params):
        return dict((param, params[param])
                    for param in self.base_params_list if param in params)

    def _perform_removal(self, files, main_path):
        for file in files:
            try:
                if os.path.isfile(file.path) or os.path.islink(file.path):
                    self._remove_file(file.path)
                    # Checking if the dir is now empty
                    file_dir = os.path.dirname(file.path)
                    if not os.listdir(file_dir) and file_dir != main_path:
                        self._remove_dir(file_dir)
                else:
                    if not os.listdir(file.path):
                        self._remove_dir(file.path)
            except OSError as e:
                print "Cannot remove %s: %s" % (file.path, e)

    def _remove_file(self, file_path):
        os.remove(file_path) if not self.test_mode\
            else self._print_removal(file_path)

    def _remove_dir(self, dir):
        os.rmdir(dir) if not self.test_mode else self._print_removal(dir)

    def _print_removal(self, file):
        print "Removing: %s" % file

    #TODO iterator/yield
    def _lists_intersection(self, list1, list2):
        """
        This intersection must preserve the order so cannot use
        set().intersection()
        """
        return [f for f in list1 if f in list2]

    #TODO iterator/yield
    def _get_all_files_sorted(self, path, filenamematch, sort_by, recurse,
                              remove_links):
        all_files = self._get_all_files(list(), path, filenamematch, recurse,
                                        remove_links)
        return self._sort_files(all_files, sort_by)

    def _get_all_files(self, current, path, filenamematch, recurse,
                       remove_links):
        for f in os.listdir(path):
            item_path = os.path.join(path, f)
            if (os.path.isfile(item_path) or (os.path.islink(item_path)
               and remove_links)) and re.search(filenamematch, f):
                current.append(file_object.FileObject(item_path))
            elif os.path.isdir(item_path) and recurse:
                current = self._get_all_files(current, item_path,
                                              filenamematch, recurse,
                                              remove_links)
        return current

    def _sort_files(self, files, sort_by):
        for f in files:
            f.time = getattr(os.stat(f.path), "st_%s" % sort_by)
        return sorted(files, key=lambda f: f.time)
