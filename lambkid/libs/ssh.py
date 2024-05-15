import os
import re
import time
import paramiko
from lambkid import log
import concurrent.futures


class ExecResult(object):
    def __init__(self, output, exit_status_code):
        self.__stdout = output
        self.__exit_status_code = exit_status_code

    def __str__(self):
        return self.__stdout

    @property
    def output(self):
        return self.__stdout

    @property
    def exit_status_code(self):
        return self.__exit_status_code


class SSHClient(object):
    def __init__(self, ip="127.0.0.1", port=22, username="root", password="", keep_alive_interval=60,
                 connect_timeout=1200):
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password
        self.__keep_alive_interval = keep_alive_interval
        self.__connect_timeout = connect_timeout
        self.__ssh = None
        self.__transport = None
        self.__scp = None
        self.__sftp = None

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    def wait_for_sshable(self, timeout=600):
        count=0
        while True:
            count+=1
            if count>(timeout/10):
                log.error(
                    f" {self.__ip}:{self.__port} | server {self.__ip} can not ssh: Error. err msg is in time {timeout} server cannot ssh.")
                return False
            try:
                if self.__connect():
                    log.info(f" {self.__ip}:{self.__port} | server {self.__ip} can ssh: OK.")
                    return True
            except Exception as e:
                log.warning(
                    f" {self.__ip}:{self.__port} | server {self.__ip} can not ssh: Error. err msg is {str(e)}")
            time.sleep(10)


    def exec(self, cmd, timeout=600,max_attempts=1):
        log.info(f" {self.__ip}:{self.__port} | begin to run cmd {cmd}, timeout is {timeout}...")
        try:
            try_times=0
            while True:
                try_times+=1
                if try_times>(timeout/10):
                    raise RuntimeError(f"after {timeout} seconds try, ssh is still not sshable.")
                if not self.__is_active():
                    self.__reconnect()
                    time.sleep(10)
                    continue
                else:
                    break
            stdin, stdout, stderr = self.__ssh.exec_command(cmd, timeout=timeout)
            exit_status_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode("utf-8")
            if exit_status_code == 0:
                log.info(f" {self.__ip}:{self.__port} | successful to run cmd {cmd}, output is {output}")
            else:
                log.warning(
                    f" {self.__ip}:{self.__port} | run cmd {cmd},exit_status_code is {exit_status_code}, output is {output},")
            rs = ExecResult(output, exit_status_code)
            return rs
        except Exception as e:
            log.error(f" {self.__ip}:{self.__port} | fail to run cmd {cmd}, err msg is {str(e)}")
            rs = ExecResult(f"fail to run cmd {cmd}: Error.err msg is {str(e)}", 255)
            return rs

    def exec_interactive(self, cmd_prompt):
        channel = self.__ssh.invoke_shell()
        rs = None
        try:
            results = []
            for elem in cmd_prompt:
                print(elem)
                command = elem[0]
                prompt = elem[1]
                channel.send(command + "\n")
                prompt = re.escape(prompt)  # 假设提示符是 "$"
                output = ""
                while not re.search(prompt, output):
                    print("---------------")
                    print(output)
                    if channel.recv_ready():
                        output += channel.recv(1024).decode("utf-8")
                results.append(output)
            rs = ExecResult("\n".join(results), 0)
        except Exception as e:
            rs = ExecResult(str(e), 255)
        finally:
            try:
                channel.close()
            except:
                pass
            return rs

    def scp_to_remote(self, local_path, remote_path):
        log.info(
            f" {self.__ip}:{self.__port} | Begin to copy file from local {local_path} to remote host {remote_path} ...")
        try:
            if not self.__is_active():
                self.__reconnect()
            if not self.__sftp or not self.__scp:
                self.__scp = paramiko.Transport((self.__ip, self.__port))
                self.__scp.connect(username=self.__username, password=self.__password)
                self.__sftp = paramiko.SFTPClient.from_transport(self.__scp)
            if os.path.isfile(local_path):
                self.__sftp.put(local_path, remote_path)
            if os.path.isdir(local_path):
                self.__sftp.mkdir(remote_path)
                for item in os.listdir(local_path):
                    local_item_path = os.path.join(local_path, item)
                    remote_item_path = os.path.join(remote_path, item)
                    self.scp_to_remote(local_item_path, remote_item_path)
            log.info(
                f" {self.__ip}:{self.__port} | Success to copy file from local {local_path} to remote host{remote_path}: OK.")
        except Exception as e:
            log.error(
                f"{self.__ip}:{self.__port} | Failed to copy file from local {local_path} to remote host {remote_path}: Error. err msg is:{str(e)}")
            raise e

    def __connect(self):
        log.info(f" {self.__ip}:{self.__port} | begin to create ssh connect...")
        try:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(hostname=self.__ip, port=self.__port, username=self.__username, password=self.__password,
                               timeout=self.__connect_timeout)
            self.__transport = self.__ssh.get_transport()
            self.__transport.set_keepalive(self.__keep_alive_interval)
            log.info(f" {self.__ip}:{self.__port} | successful to create ssh connect: OK.")
            return True
        except Exception as e:
            log.warning(f" {self.__ip}:{self.__port} | fail create ssh connect: Error.err msg is {str(e)}")
            return False

    def __reconnect(self):
        try:
            if self.__ssh:
                del self.__ssh
        except:
            pass
        return self.__connect()

    def __is_active(self):
        try:
            if not self.__transport:
                return False
            is_active = self.__transport.is_active()
            if is_active:
                log.info(f" {self.__ip}:{self.__port} | ssh channel is active.")
                return True
            else:
                log.info(f" {self.__ip}:{self.__port} | ssh channel is not active.")
                return False
        except Exception as e:
            log.warning(f" {self.__ip}:{self.__port} | fail to get ssh channel status: Error.err msg is {str(e)}")
            return False
