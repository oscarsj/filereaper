==========
filereaper
==========

Note: this tool is still in development, there are some pending things to do like:
 * implement more policies
 * code documentation
 * add readme documentation
 * pep8 fixes
 * implement missing options

About
---------

Filereaper is a tool to remove files based on different and flexible policies.


Installation
-------------

Two installation modes, the regular one is by a Debian package, the development one is as a Python egg

Modes
--------

Filereaper can work in two different ways.

 * As a command line executor:
   Just executing filereaper by command line passing the corresponding parameters specifying file regexp, policies, etc.

   Example: Remove recursively files in /var/log/apache that matchs \*.log keeping always a minimum of 2 files and removing the ones older than 20 days, being the files ordered by access time.

   filereaper --keepminimum 2 --file_match "\*.log" --recurse true --time_mode atime --older_than_d 20 /var/log/apache

 * As a self configured crons:
   This mode configure the Linux crontabs by specifying some configuration files. The idea is to have a configuration file per directory to clean.

   By default, you will only need to add configuration files to /etc/filereaper/conf.d/ similar to the samples provided in conf directory.

   Filereaper will configure the system crontabs to based on these configuration files, also, it has a storage layer so it remembers what is configured and the crontabs will always be in sync with the configuration files.


Policies
---------

The policies are applies in the most restrictive way, this means removing the less as possible for security reasons. Therefore if a policy says to remove A and B files and another policy says to remove A and C, only A will be removed.

 * keeplast: ordering by time (atime, ctime or mtime) filereaper will remove everything but the N last specified here.

 * older_than_d: ordering by time (atime, ctime or mtime) filreaper will remove the files older than N days

