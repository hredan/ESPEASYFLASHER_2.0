"""
  build_info.py is a script to generate system environment data.
  This data are helpful for error analysis of EEF.

  For help use:
  python ./build_info.py -h

  Copyright (C) 2022  André Herrmann
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import platform
import getopt
from pkg_resources import working_set

HELP = r"""Paramter:
-s\tGITHUB_SHA
-r\tGITHUB_REPOSITORY
-t\tTAG_NAME
e.g. python ./build_info.py -s \$GITHUB_SHA -r \$GITHUB_REPOSITORY"""


def create_info_file(repo_name, tag_name, sha):
    """ generates the build_info.txt with GitHub and system environment data """
    packages = working_set.by_key
    sorted_package_names = sorted(packages.keys())

    with open('build_info.txt', 'w', encoding="utf-8") as info_file:
        if repo_name:
            info_file.write('Repository URL:  www.github.com/' + repo_name + '\n')
        if sha:
            info_file.write('GITHUB_SHA:      ' + sha + '\n')
        if tag_name:
            info_file.write('Release version: ' + tag_name + '\n')

        info_file.write('OS:              ' + platform.system() +
                platform.release() + '\n')
        info_file.write('Pyhton Version:  ' + sys.version + '\n')
        info_file.write('PIP list: \n')
        for name in sorted_package_names:
            info_file.write(f'\t{packages[name].key} {packages[name].version}\n')


def main(argv):
    """ main function with arguments, see help"""
    repo_name = ''
    tag_name = ''
    sha = ''

    try:
        opts = getopt.getopt(argv, "hs:r:t:")
    except getopt.GetoptError as err:
        print("Error:")
        print(err)
        print("use:")
        print(HELP)
        sys.exit(2)
    for opt, arg in opts[0]:
        if opt == '-h':
            print(HELP)
            sys.exit(0)
        elif opt == "-r":
            repo_name = arg
        elif opt == "-t":
            tag_name = arg
        elif opt == "-s":
            sha = arg
    create_info_file(repo_name, tag_name, sha)


if __name__ == "__main__":
    main(sys.argv[1:])
