#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os
import sys
import json
import time

class FtpClient(object):
    def __init__(self):
        self.ip_port = ('127.0.0.1',8010)
        self.sk = socket.socket()
        self.sk.connect(self.ip_port)

    def handler(self):
        while True:
            username = raw_input("username : ").strip()
            password = raw_input("password : ").strip()
            if username is None or password is None:
                print 'Please input the right username and password !!!'
                continue
            else:
                data = {
                    'action' : 'login',
                    'username' : username,
                    'password' : password
                }
                self.sk.sendall(json.dumps(data))
                response = self.sk.recv(4096)
                status , msg = json.loads(response)
                print status,msg
                if response:
                    while True:
                        command = raw_input('%s--->' % os.getcwd()).strip()
                        if  command == 'ls' or command == 'dir':
                            command_list = command.split()
                            data = ''
                            if len(command_list) == 1:
                                data = {
                                        'action': 'listdir',
                                        }
                            elif len(command_list) == 2:
                                data = {
                                        'action': 'listdir',
                                        'directory':command_list[1],
                                        }
                            self.sk.sendall(json.dumps(data))
                            data = self.sk.recv(1024)
                            status,msg = json.loads(data)
                            if status:
                                for k,v in msg:
                                    print '%s --------------- %s' % (k,v)
                        elif command == 'pwd':
                            data = {
                                    'action': 'getpwd',
                                    }
                            self.sk.sendall(json.dumps(data))
                            data = self.sk.recv(4096)
                            status,msg = json.loads(data)
                            if status:
                                print msg

                        elif command == 'lcd':
                            print 'local dir : %s'  % os.getcwd()


                        elif command.startswith('get'):
                            command_list = command.split()
                            if len(command_list) <> 2:
                                print 'Please input the right command !!!!'
                            else:
                                data = {
                                    'action':'getfile',
                                    'file_name' : command_list[1]
                                }
                                self.sk.sendall(json.dumps(data))
                                response = self.sk.recv(4096)
                                response = json.loads(response)
                                if response['status'] == 'ready':
                                    file_size = response['file_size']
                                    file_size = int(file_size)
                                    self.sk.sendall('begin')
                                    received = 0
                                    with open(command_list[1],'wb') as f:
                                        while True:
                                            data = self.sk.recv(524288)
                                            f.write(data)
                                            received += len(data)
                                            percent = float(received)/float(file_size)*100
                                            percent = int(percent)
                                            sys.stdout.write('\r'+'#'*percent+'%'+'%d' % percent)
                                            time.sleep(0.1)
                                            if received >= file_size:
                                                break
                                    self.sk.sendall('finish')
                                    data = self.sk.recv(1024)
                                    status,msg = json.loads(data)
                                    if status:
                                        print
                                        print msg
                        elif command.startswith('put'):
                            command_list = command.split()
                            if len(command_list) <> 2:
                                print 'Please input the right command !!!!'
                            else:
                                file_name = command_list[1]
                                if os.path.isfile(file_name):
                                    file_size = os.path.getsize(file_name)
                                    data = {
                                        'action':'putfile',
                                        'file_name' : file_name,
                                        'file_size' : file_size,
                                    }
                                    self.sk.sendall(json.dumps(data))
                                    response = self.sk.recv(4096)
                                    status,msg = json.loads(response)
                                    if status:
                                        sended = 0
                                        with open(file_name,'rb') as f:
                                            while True:
                                                data = f.read(1024)
                                                self.sk.send(data)
                                                sended += len(data)
                                                if sended >= file_size:break
                                        response = self.sk.recv(1024)
                                        status,msg = json.loads(response)
                                        if status:
                                            print msg
                                    else:
                                        print msg
                        elif command.startswith('cd'):
                            command_list = command.split()
                            if len(command_list) <> 2:
                                print 'Please input the right command !!!!'
                            else:
                                dir_name = command_list[1]
                                data = {
                                    'action' :  'switchfolder',
                                    'dir_name' : dir_name
                                }
                                self.sk.sendall(json.dumps(data))
                                response = self.sk.recv(1024)
                                status,obj = json.loads(response)
                                print obj
                else:
                    print msg


    def disconnect(self):
        self.sk.close()
    def login(self):
        pass



if __name__ == '__main__':
    ftpclient = FtpClient()
    ftpclient.handler()
