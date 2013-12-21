==========
filereaper
==========

Note: this tool is still in development, there are some pending things to do like:

 * implement more policies
 * code documentation
 * implement missing options

About
---------

Filereaper is a tool to remove files based on different and flexible policies.


Installation
-------------

Two installation modes:
 * Debian package: regular installation
 * Python egg: for development

Execution modes
---------------

Filereaper can work in two different ways.

 * **As a command line executor**:

   Just executing filereaper by command line passing the corresponding parameters specifying file regexp, policies, etc.

   Example: Remove recursively files in /var/log/apache that matchs \*.log keeping always a minimum of 2 files and removing the ones older than 20 days, being the files ordered by access time.

   $ filereaper --keepminimum 2 --file_match "\*.log" --recurse true --time_mode atime --older_than_d 20 --exclude_list main.log,main2.log --test_mode False /var/log/apache

 * **As a self configured crons**:

   This mode configure the Linux crontabs by specifying some configuration files. The idea is to have a configuration file per directory to clean.

   By default, you will only need to add configuration files to /etc/filereaper/conf.d/ similar to the samples provided in conf directory.

   Filereaper will configure the system crontabs to based on these configuration files, also, it has a storage layer so it remembers what is configured and the crontabs will always be in sync with the configuration files.


Parameters
----------

 * **test_mode**

   Security parameter activated by default that prints the files to be removed instead of removing them. This is useful while testing your configuration/command line. Once you are sure it's correct, disable this parameter and filereaper will perform the removal instead of printing them.

   Default: True (activated)

 * **exclude_list**

   Separated comma list with the files to exclude from the removal

   Default: "" (empty)

 * **file_match**

   Only files that match this regexp

   Default: ".*" (match everything)

 * **keepminimum**

   Setting this parameter assures filereaper will always keep at least N minimum files. This parameter has higher priority than any policy.

   Default: 0 

 * **recurse**

   Perform the removal recursively. The policies are applied to the full list of files gathered recursively.

   Default: False

 * **remove_links**

   If activated, filereaper removes symlinks. Only the symlink, not the file/dir were it points.

   Default: False

 * **time_mode**

   Parameter used when ordering the files, the possible values are atime (access time), ctime (creation time), mtime (modification time)

   Default: ctime


Policies
---------

The policies are applies in the most restrictive way, this means removing the less as possible for security reasons. Therefore if a policy says to remove A and B files and another policy says to remove A and C, only A will be removed.

 * **keeplast**

  ordering by time (atime, ctime or mtime) filereaper will remove everything but the N last specified here.

 * **older_than_d**

  ordering by time (atime, ctime or mtime) filreaper will remove the files older than N days