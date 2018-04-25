import os
import hashlib
import configparser


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


class FileDir(object):
    def __init__(self, path):
        config = get_config("client.conf")
        self.path = path
        self.block_size = int(config['FILE']['block_size'])

    def get_metadata(self):
        """
            Return dict of metadata
        """
        data = {'name': os.path.basename(self.path), 'path': os.path.abspath(self.path), 'attr': os.stat(self.path)}
        if os.path.isdir(self.path):
            data['type'] = "directory"

        elif os.path.islink(self.path):
            real_path = os.path.realpath(self.path)
            data['type'] = "symlink"
            data['real_path'] = real_path
            if os.path.exists(real_path):
                data['checksum'] = md5(real_path)
        elif os.path.isfile(self.path):
            data['type'] = "file"
            data['checksum'] = self.list_checksum()
        elif os.path.ismount(self.path):
            data['type'] = "mount"
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
