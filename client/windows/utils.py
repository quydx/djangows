import os
import hashlib
import configparser
import psutil
import subprocess
import logging.config
import yaml
import platform


def setup_logging(default_path='logging.yaml', default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_acl(path):
    """ 
    Get acl of a path 
    Returns list added rules
    """
    
    aclfile = "aclfile.txt"
    output = subprocess.check_output(['icacls', path, "/save", aclfile])
    acl_rules = open(aclfile, 'rb').read()
    os.remove(aclfile)
    return acl_rules


def set_acl(path, acl_rules):
    """ 
    set acl of a path 
    Input : get_acl function 
    """

    aclfile = "aclfile.txt"
    open(aclfile, 'wb').write(acl_rules)
    path_root = os.path.dirname(os.path.abspath(path))
    output = subprocess.check_output(['icacls', path_root, "/restore", aclfile])
    os.remove(aclfile)
    return 0


def get_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def md5(real_path):
    """
        Return md5 hash of the file
    """
    hash_md5 = hashlib.md5()
    with open(real_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_in_blocks(file_object, blk_list, block_size):
    block_id = 0
    while True:
        data = file_object.read(block_size)
        if not data:
            break
        if block_id in blk_list:
            yield (data, block_id)
        block_id += 1 
    file_object.close()


def cutting_blocks(path, blk_list_save, block_size):
    data_save = []
    file_read = open(path, 'rb')
    data_save = [item[0] for item in read_in_blocks(file_read, blk_list_save, block_size)]
    
    file_write = open(path, 'wb')
    for chunk in data_save:
        file_write.write(chunk)
    file_write.close()


def get_info_agent():
    mem = psutil.virtual_memory().total / (1024**3)
    data = {"cpus": psutil.cpu_count(), "platform": platform.platform(), "mem_total": round(mem,2)}
    return data


class FileDir(object):
    def __init__(self, path, block_size):
        self.path = path
        self.block_size = block_size
    def get_fs_type(self):
        partition = {}
        for part in psutil.disk_partitions():
            partition[part.mountpoint] = part.fstype
        if self.path in partition:
            return partition[self.path]
        splitpath = self.path.split(os.sep)  
        for i in range(len(splitpath),0,-1):
            path = os.sep.join(splitpath[:i]) + os.sep
            if path in partition:
                return partition[path]
            path = os.sep.join(splitpath[:i])
            if path in partition:
                return partition[path]
        return "unknown"
        
    def get_metadata(self):
        """
            Return dict of metadata
        """
        data = {'name': os.path.basename(self.path), 'path': os.path.abspath(self.path), 'fs': self.get_fs_type(), 'attr':{}}
        if os.path.islink(self.path):
            real_path = os.path.realpath(self.path)
            data['type'] = "symlink"
            data['real_path'] = real_path
            if os.path.exists(real_path):
                data['checksum'] = md5(real_path)
            return data

        # Permission 
        stat = os.stat(self.path)
        attr = {}
        attr['access_time'] = stat.st_atime  # access time
        attr['modify_time'] = stat.st_mtime  # modify time
        attr['create_time'] = stat.st_ctime  # create time
        attr['uid'] = stat.st_uid            # user ID
        attr['gid'] = stat.st_gid            # group ID
        attr['mode'] = stat.st_mode          # inode protection mode

        # ACL
        attr['acl'] = get_acl(self.path)

        data['attr'] = attr

        if os.path.isdir(self.path):
            data['type'] = "directory"
        elif os.path.isfile(self.path):
            data['type'] = "file"
            data['checksum'] = self.list_checksum()
        else:
            raise TypeError("Type of object")
        return data

    def list_checksum(self):
        """
            Return list checksum of file separated by block size
        """
        hash_md5 = hashlib.md5()
        checksum_list = []
        with open(self.path, 'rb') as file:
            chunk = file.read(self.block_size)
            while len(chunk) > 0:
                hash_md5.update(chunk)
                checksum_list.append(hash_md5.hexdigest())
                chunk = file.read(self.block_size)
        return checksum_list
