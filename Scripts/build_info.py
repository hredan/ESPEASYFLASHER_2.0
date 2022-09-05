import sys
import platform
import pkg_resources
import getopt

HELP="""Paramter:
-s\tGITHUB_SHA
-r\tGITHUB_REPOSITORY
-t\tTAG_NAME
e.g. python ./build_info.py -s \$GITHUB_SHA -r \$GITHUB_REPOSITORY"""

def create_info_file(repo_name, tag_name, sha):
    print(f"{repo_name}, {tag_name} ,{sha}")
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

    with open('build_info.txt', 'w') as f:
        if(repo_name):
          f.write('Repository URL:  www.github.com/' + repo_name + '\n')
        if(sha):
          f.write('GITHUB_SHA:      ' + sha + '\n')
        if(tag_name):
          f.write('Release version: ' + tag_name + '\n')

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
      opts, args = getopt.getopt(argv,"hs:r:t:")
    except getopt.GetoptError as err:
      print("Error:")
      print(err)
      print("use:")
      print(HELP)
      sys.exit(2)
    print(opts)
    for opt, arg in opts:
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