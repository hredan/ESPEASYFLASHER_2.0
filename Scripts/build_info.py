import sys
import platform
import pkg_resources
import getopt

HELP="""Paramter:
-s\tGITHUB_SHA
-r\tGITHUB_REPOSITORY
-t\tTAG_NAME
e.g. python ./build_info.py -s \$GITHUB_SHA -r \$GITHUB_REPOSITORY"""

def create_info_file():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

    with open('build_info.txt', 'w') as f:
        f.write('OS: ' + platform.system() + platform.release() + '\n')
        f.write('Pyhton Version: ' + sys.version + '\n')
        f.write('PIP list: \n')
        for package in installed_packages_list:
            f.write('\t' + package + '\n')

def main(argv):
    repo_name = ''
    tag_name = ''
    sha = ''

    try:
      opts, args = getopt.getopt(argv,"hsrt",["ifile=","ofile="])
    except getopt.GetoptError:
      print(HELP)
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print(HELP)

if __name__ == "__main__":
   main(sys.argv[1:])