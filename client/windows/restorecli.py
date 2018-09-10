#!C:\Program Files (x86)\Python37-32 
import os
from restore import main
import argparse


parser = argparse.ArgumentParser(description="Run the Backup CLI")
parser.add_argument('-c', '--config-file', dest='config_file', default='client.conf',
                    help='Path of config file')
parser.add_argument('-t', '--target', dest='repo_targets', required=True, nargs = '*',
                    help='Path of directory need to backup')
parser.add_argument('-s', '--server', dest='server_address',
                    help='Server backup')             
parser.add_argument('-p', '--pk', dest='backup_id', required=True, nargs = '*',
                    help='Primary key need to backup')     
parser.add_argument('-j', dest='job_id', default=None,
                    help='Job in controller') 

args = parser.parse_args()

# check file config
if os.path.exists(args.config_file):
    pass
else: 
    print("File config does not exist ")
    exit(1)

# Input multi repo_target and backup_id  
for index, repo_target in enumerate(args.repo_targets):
    bid = args.backup_id[index]

    # check type pk is `number`
    try:
        val = int(bid)
    except ValueError:
        print("PK's not an int!") 
        exit(1)

    if repo_target and repo_target.endswith('\\'):
        repo_target = repo_target[:len(repo_target)-1]
    main(args, repo_target, bid)
