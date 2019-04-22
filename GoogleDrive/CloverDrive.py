# coding:utf-8
import os
import sys
import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class CloverDrive:

    def __init__(self):
        credentials = "credentials.json"
        gauth = GoogleAuth()
        if os.path.exists(credentials):
            gauth.LoadCredentialsFile(credentials)
        else:
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(credentials)
        self.drive = GoogleDrive(gauth)
        try:
            self.cudir = [self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()[
                0]['parents'][0]['id']]  # current directory stack
        except IndexError:
            print("No directory in drive.")

    def command(self):
        pat = re.compile("\s+")
        print(">>", end="")
        cmd = input()
        cmd = pat.split(cmd)
        if cmd[0] in {'exit', 'quit'}:
            sys.exit()
        elif cmd[0] in {'up', 'upload'}:
            self.upload(cmd[1:])
        elif cmd[0] in {'dl', 'download'}:
            self.download(cmd[1:])
        elif cmd[0] in {'rm', 'remove', 'delete'}:
            self.remove(cmd[1:])
        elif cmd[0] in {'cd'}:
            self.chdir(cmd[1:])
        elif cmd[0] in {'ls', 'dir'}:
            self.ls()
        else:
            print("Unknown Command: " + cmd[0])

    def upload(self, path_list):
        for path in path_list:
            try:
                f = self.drive.CreateFile({'parents': [
                                          {'kind': "drive#fileLink", 'id': self.cudir[-1]}], 'title': os.path.basename(path)})
                f.SetContentFile(path)
                print("Uploading...")
                f.Upload()
                print("Uploaded: " + os.path.basename(path))
            except FileNotFoundError:
                print("Can't find files.")
            except:
                print("###UPLOAD ERROR###: " + os.path.basename(path))

    def download(self, id_list):
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.cudir[-1])}).GetList()
        for id in id_list:
            if id.isdigit():
                try:
                    print("Downloading...")
                    file_list[int(id)].GetContentFile(
                        file_list[int(id)]['title'])
                    print("Downloaded: " + file_list[int(id)]['title'])
                except IndexError:
                    print("Index out of range.")
                except:
                    print("###DOWNLOAD ERROR###: ")
            else:
                print("Unknown Index: " + id)

    def remove(self, id_list):
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.cudir[-1])}).GetList()
        for id in id_list:
            if id.isdigit():
                try:
                    file_list[int(id)].Trash()
                    print("Deleted: " + file_list[int(id)]['title'])
                except IndexError:
                    print("Index out of range.")
            else:
                print("Unknown Index: " + id)

    def chdir(self, id_list):
        for id in id_list:
            file_list = self.drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format(self.cudir[-1])}).GetList()
            if id == '/':
                self.cudir = [self.cudir[0]]
            elif id == '..':
                if len(self.cudir) != 1:
                    self.cudir = self.cudir[:-1]
            elif id.isdigit():
                try:
                    self.cudir.append(file_list[int(id)]['id'])
                except IndexError:
                    print("Index out of range.")
            else:
                print("Unknown Index: " + id)
            break

    def ls(self):
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.cudir[-1])}).GetList()
        for i, f in enumerate(file_list):
            print("[%d] %s" % (i, f['title']))


def main():
    cd = CloverDrive()
    while True:
        cd.command()

if __name__ == '__main__':
    main()
