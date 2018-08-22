#!C:\Program Files (x86)\Python37-32 
import os
from restore import main
import argparse


parser = argparse.ArgumentParser(description="Run the Backup CLI")
parser.add_argument('--config-file', dest='config_file', default='client.conf',
                    help='Path of config file')
parser.add_argument('--target', dest='repo_target', required=True,
                    help='Path of directory need to backup')
parser.add_argument('--version', dest='version', required=True,
                    help='Version need to backup')                                 
args = parser.parse_args()

# check file config
if os.path.exists(args.config_file):
    pass
else: 
    print("File config does not exist ")
    exit(1)


# check type version is `number`
try:
    val = int(args.version)
except ValueError:
    print("Version's not an int!") 
    exit(1)
    
if args.repo_target and args.repo_target.endswith('\\'):
    args.repo_target = args.repo_target[:len(args.repo_target)-1]
main(args)
