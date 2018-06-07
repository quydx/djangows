import os
import hashlib
import configparser
import psutil
import subprocess


def get_file_acl(path):
    """ get dict of acl  of a path
    """
    acl = dict()
    getacl = subprocess.call(['which','getfacl'])
    if getacl == 0:
        return False
    else:
        output = subprocess.check_output(['getfacl', path])
        lines = output.stdout.decode('utf-8').splitlines()
        user, group, other = [], [], []
        for line in lines:
            acl_item = tuple(line.split('::'))
            if line.startswith('user'):
                user.append(acl_item)
            elif line.startswith('group'):
                group.append(acl_item)
            elif line.startswith('other'):
                other.append(acl_item)
        acl['user'] = user
        acl['group'] = group
        acl['other'] = other
    return acl


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


def read_in_blocks(file_object, blk_list):
    block_id = 0
    while True:
        data = file_object.read(block_size)
        if not data:
            break
        if block_id in blk_list:
            yield (data, block_id)
        block_id += 1 
    file_object.close()


def cutting_blocks(path, blk_list_save):
    data_save = []
    file_read = open(path, 'rb')
    data_save = [item[0] for item in read_in_blocks(file_read, blk_list_save)]
    
    file_write = open(path, 'wb')
    for chunk in data_save:
        file_write.write(chunk)
    file_write.close()


class FileDir(object):
    def __init__(self, path):
        
        self.path = path
        

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

        stat = os.stat(self.path)
        attr = {}
        attr['access_time'] = stat.st_atime  # access time
        attr['modify_time'] = stat.st_mtime  # modify time
        attr['create_time'] = stat.st_ctime  # create time
        attr['uid'] = stat.st_uid            # user ID
        attr['gid'] = stat.st_gid            # group ID
        attr['size'] = stat.st_size          # size
        attr['nlink'] = stat.st_nlink        # number of hard links
        attr['inode'] = stat.st_ino          # inode number
        attr['device'] = stat.st_dev         # device inode resides on.
        attr['mode'] = stat.st_mode          # inode protection mode

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
            chunk = file.read(block_size)
            while len(chunk) > 0:
                hash_md5.update(chunk)
                checksum_list.append(hash_md5.hexdigest())
                chunk = file.read(block_size)
        return checksum_list


config = get_config("client.conf")
block_size = int(config['FILE']['block_size'])

