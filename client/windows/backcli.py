#!C:\Program Files (x86)\Python37-32
import os
from backup import main
import argparse


parser = argparse.ArgumentParser(description="Run the Backup CLI")
parser.add_argument('-c', '--config-file', dest='config_file', default="E:\\Huyen Trang\\project\\djangows\\client\\windows\\client.conf",
                    help='Path of config file')
parser.add_argument('-t', dest='repo_targets', required=True, nargs = '*',
                    help='Path of directory need to backup')
parser.add_argument('-s', dest='server_address',
                    help='Server backup')                 
parser.add_argument('-j', dest='job_id',
                    help='Job in controller')     


args = parser.parse_args()
print(args)

if os.path.exists(args.config_file):
    pass
else:
    print("File config does not exist ")
    exit(1)

for repo_target in args.repo_targets:
    if os.path.exists(repo_target):
        if repo_target.endswith('\\'):
            repo_target = repo_target[:len(repo_target)-1]
        main(args, repo_target)
    else:
        err = "Specified path does not exist"
        main(args, repo_target, err)
        print(err)
