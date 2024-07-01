import os
import re
import time
import traceback
import threading
import queue
from lambkid import log
from fabric import Connection
from invoke import Responder
from func_timeout import func_set_timeout

class ExecResult(object):
    def __init__(self, output, exit_status_code,stderr=""):
        self.__stdout = output
        self.__exit_status_code = exit_status_code
        self.__stderr=stderr

    def __str__(self):
        return self.__stdout

    def stdout(self):
        return self.__stdout

    def stderr(self):
        return self.__stderr

    @property
    def output(self):
        return self.__stdout

    @property
    def exit_status_code(self):
        return self.__exit_status_code


class SSHClient(object):
    def __init__(self, ip="127.0.0.1", port=22, username="root", password="",connect_timeout=10):
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password
        self.__connect_timeout = connect_timeout
        self.__ssh = None
        self.__is_active=False
    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    def wait_for_sshable(self, timeout=600):
        count=0
        while True:
            count+=1
            if count>(timeout/10):
                log.error(
                    f" {self.__ip}:{self.__port} | server {self.__ip} can not ssh: Error. err msg is in time {timeout} server cannot ssh.")
                return False
            try:
                output=self.exec("ls /").output
                if "root" in output.strip():
                    return True
            except Exception as e:
                log.warning(
                    f" {self.__ip}:{self.__port} | server {self.__ip} can not ssh: Error. err msg is {str(e)}")
            time.sleep(10)

    @func_set_timeout(3600)
    def _exec(self, cmd):
        log.info(f" {self.__ip}:{self.__port} | begin to run cmd {cmd}...")
        if not self.__is_active:
            self.__connect()
        try:
            rs=self.__ssh.run(cmd)
            if rs.return_code == 0:
                log.info(f" {self.__ip}:{self.__port} | successful to run cmd {cmd}, output is {rs.stdout.strip()}")
            else:
                log.warning(
                    f" {self.__ip}:{self.__port} | run cmd {cmd},exit_status_code is {rs.return_code}, output is {rs.stdout.strip()},")
            new_rs = ExecResult(rs.stdout.strip(), rs.return_code)
        except Exception as e:
            self.__is_active = False
            new_rs = ExecResult(str(e),255)
        return new_rs

    def exec(self, cmd,timeout=1800):
        return self._exec(cmd)

    def exec_interactive(self, cmd,promt_response=[]):
        if not self.__is_active:
            self.__connect()
        response_list=[]
        for elem in promt_response:
            prompt=elem["prompt"]
            response=elem["response"]
            responser = Responder(
                pattern=prompt,
                response=response + '\n',
            )
            response_list.append(responser)
        rs = self.__ssh.run(cmd, pty=True, watchers=response_list)
        new_rs = ExecResult(rs.stdout.strip(),rs.return_code)
        return new_rs


    def scp_to_remote(self, local_path, remote_path):
        log.info(
        f" {self.__ip}:{self.__port} | Begin to copy file from local {local_path} to remote host {remote_path} ...")
        if not self.__is_active:
            self.__connect()
        self.__ssh.put(local_path,remote_path)
        log.info(
            f" {self.__ip}:{self.__port} | Success to copy file from local {local_path} to remote host{remote_path}: OK.")

    def scp_file_to_local(self, remote_path, local_path):
        log.info(
            f" {self.__ip}:{self.__port} | Begin to copy file from remote {remote_path} to local host {local_path} ...")
        if not self.__is_active:
            self.__connect()
        if os.path.isfile(local_path):
            os.system(f"rm -rf {local_path}")
        self.__ssh.get(remote=remote_path,local=local_path)
        log.info(
            f" {self.__ip}:{self.__port} | Success to copy file from remote {remote_path} to local host{local_path}: OK.")

    def __connect(self):
        log.info(f" {self.__ip}:{self.__port} | begin to create ssh connect...")
        try:
            self.__ssh = Connection(host=self.__ip, port=self.__port, user=self.__username, connect_kwargs={"password": self.__password},
                      connect_timeout=self.__connect_timeout)
            log.info(f" {self.__ip}:{self.__port} | successful to create ssh connect: OK.")
            self.__is_active=True
            return True
        except Exception as e:
            log.error(f" {self.__ip}:{self.__port} | fail create ssh connect: Error.err msg is {str(e)}",exc_info=True)
            self.__is_active = False
            return False

    def __del__(self):
        try:
            self.__ssh.close()
        except:
            pass