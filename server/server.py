#!/usr/bin/env python
# -*- coding:utf-8 -*-

import SocketServer
import subprocess
import re
import os
import json
from module import auth
import sys
BASE_DIR = os.path.dirname( os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from conf import settings




class FtpServer(SocketServer.BaseRequestHandler):

    def handle(self):
        print self.client_address
        self.conn = self.request
        while True:
            data = self.conn.recv(1024)
            data = json.loads(data)
            operation =  data['action']
            if hasattr(self,operation):
                func = getattr(self, data['action'])
                results = func(data)
                self.conn.sendall(json.dumps(results))
                continue
            else:
                data = {
                    'action': 'failed',
                    'msg' : 'input the right parameter !!'
                }

    def listdir(self,data):
        filelist = []
        if data.has_key('directory'):
            pass
        else:
            for i in  os.listdir(os.getcwd()):
                if os.path.isdir(i):
                    temp = ('dir',i)
                    filelist.append(temp)
                elif os.path.isfile(i):
                    temp = ('file',i)
                    filelist.append(temp)
            return True,filelist

    def getpwd(self,data):
        return True,'remote dir : %s' % os.getcwd()

    def getfile(self,data):
        file_name = data.get('file_name')
        if os.path.isfile(file_name):
            file_size = os.path.getsize(file_name)
            response = {
                'status': 'ready',
                'file_size' : str(file_size)
            }
            self.conn.sendall(json.dumps(response))
            data = self.conn.recv(1024)
            if data == 'begin':
                with open(file_name,'rb') as f:
                    while True:
                        data = f.read(524288)
                        if data:
                            self.conn.sendall(data)
                        else:
                            break
                data = self.conn.recv(1024)
                if data == 'finish':
                    return True,'finish'
        else:
            response = {'status':False,'msg':'file not exist!!!'}
            return response

    def getbrokenfile(self,data):
        file_name = data.get('file_name')
        file_size = os.path.getsize(file_name)
        broken_file_size = data.get('broken_file_size')
        broken_file_size = int(broken_file_size)
        print broken_file_size
        sended = broken_file_size
        response = {
            'file_size':file_size,
        }
        self.conn.send(json.dumps(response))
        with open(file_name,'rb') as f:
            f.seek(broken_file_size)
            while True:
                data = f.read(524288)
                self.conn.send(data)
                sended += len(data)
                if sended >= file_size:
                    break
            response = self.conn.recv(1024)
            if response== 'finish':
                return True,'ok'
    def FileSize(self,path):
        size = 0L
        for root , dirs, files in os.walk(path, True):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
            #目录下文件大小累加
        return size

    def putfile(self,data):

        file_size = int(data['file_size'])
        total_size = self.FileSize(self.home_dir)
        response = ''

        if (total_size+file_size) >= self.quota *1024*1024:
            response = False,'your reach the quota !!!!!!!'
            return response
        else:
            response = True,'ok'
        self.conn.sendall(json.dumps(response))
        received = 0
        with open(data['file_name'] , 'wb ') as f:
            while True:
                data = self.conn.recv(524288)
                f.write(data)
                received +=len(data)
                if received >= file_size:
                    break
        return True,'finish'

    def switchfolder(self,data):
        os.path.abspath(os.path.join(os.path.abspath('.'),))
        if os.path.isdir(data['dir_name']):
            after_channge_dir = os.path.abspath(os.path.join(os.path.abspath('.'),data['dir_name']))
            if after_channge_dir.startswith(os.path.join(settings.USER_BASE,self.username)):
                os.chdir(data['dir_name'])
                return True,os.getcwd()
            else:
                return False,''' Only in your home dir!!!!!'''

        else:
            return False,'this is not a dir!!!!!'

    def login(self,data):
        os.chdir(settings.USER_BASE)
        username = data['username']
        password = data['password']
        status,msg,quota = auth.authenticate(username,password)
        data = {
            'status' : status,
            'msg':msg
        }
        if status:
            self.username = username
            self.home_dir = os.path.join(settings.USER_BASE,username)
            self.quota = quota
            if not os.path.exists(self.home_dir):
                os.makedirs(self.home_dir)
            os.chdir(self.home_dir)
            data['home_dir'] = self.home_dir

        return data
if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('127.0.0.1',8010),FtpServer)
    server.serve_forever()