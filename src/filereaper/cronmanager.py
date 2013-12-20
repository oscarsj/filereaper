import os

from jinja2 import Template

CRON_TEMPLATE = """#!/bin/bash

# File added by filereaper, do not change nor remove this file,
# remove its configuration file instead and reload filereaper.

{{run_with_pre}}{{executor}} {{params}}{{run_with_post}}
"""

class CronManager(object):

    executor = None
    crons_path = None
    crons_prefix = None

    def __init__(self, executor, crons_path, crons_prefix):
        self.executor = executor
        self.crons_path = crons_path
        self.crons_prefix = crons_prefix

    def load(self, module):
        params = ""
        run_with = module.run_with if hasattr(module, 'run_with') else None
        for attr in module.attributes:
            value = getattr(module, attr)
            if isinstance(value, bool) and value:
                params+="--%s " % attr
            else:
                params+="--%s %s " % (attr, value)
        run_with_pre = ""
        run_with_post = ""
        if run_with:
            run_with_pre = "sudo -u %s sh -c \"" % run_with
            run_with_post = '"'

        template = Template(CRON_TEMPLATE)
        content = template.render(run_with_pre = run_with_pre,
                        run_with_post = run_with_post,
                        executor = self.executor,
                        params = params)

        with open(os.path.join(self.crons_path,
                               '%s_%s' % (self.crons_prefix,
                                          module.name.replace(' ', '_'))),
                  'w') as f:
            f.write(content)
