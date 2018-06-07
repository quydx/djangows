#!C:\Users\Huyen Trang\AppData\Local\Programs\Python\Python36
import os
from backup import main
import argparse


parser = argparse.ArgumentParser(description="Run the Backup CLI")
parser.add_argument('--config-file', dest='config_file', default='client_vnu.conf',
                    help='Path of config file')
parser.add_argument('--target', dest='repo_target', required=True,
                    help='Path of directory need to backup')                    
args = parser.parse_args()

if os.path.exists(args.config_file):
    pass
else: 
    print("File config does not exist ")
    exit(1)

if os.path.exists(args.repo_target):
    if args.repo_target.endswith('\\'):
        args.repo_target = args.repo_target[:len(args.repo_target)-1]
    # if args.repo_target[0].islower(): # chua chac 
        # args.repo_target =  chuyen thanh chu hoa 
        pass 
    main(args)
else:
    print("Specified path does not exist ")
