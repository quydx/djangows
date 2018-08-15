#!C:\Program Files (x86)\Python37-32
import os
from backup import main
import argparse


parser = argparse.ArgumentParser(description="Run the Backup CLI")
parser.add_argument('--config-file', dest='config_file', default='client.conf',
                    help='Path of config file')
parser.add_argument('-t', dest='repo_target', required=True,
                    help='Path of directory need to backup')
parser.add_argument('-s', dest='server_address',
                    help='Server backup')                 
parser.add_argument('-j', dest='job_id',
                    help='Job in controller')     


args = parser.parse_args()

if os.path.exists(args.config_file):
    pass
else:
    print("File config does not exist ")
    exit(1)

if os.path.exists(args.repo_target):
    if args.repo_target.endswith('/'):
        args.repo_target = args.repo_target[:len(args.repo_target)-1]
    main(args)
else:
    err = "Specified path does not exist"
    main(args, err)
    print(err)