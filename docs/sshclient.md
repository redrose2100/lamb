# usage of sshclient in lambkid

## usage of sshclient

* usage 1: check out whether remote host can ssh

```python 
from lambkid import SSHClient


ssh=SSHClient(ip="127.0.0.1",port=22,username="root",password="root@123")
sshable=ssh.wait_for_sshable(1800)   # check whether remote host can ssh,timeout is 1800 seconds
```

* usage 2: run command in remote host

```python
from lambkid import SSHClient

ssh = SSHClient(ip="127.0.0.1", port=22, username="root", password="root@123")
rs = ssh.exec("ls /opt")
print(rs.output)  # display of command run in remote host
print(rs.exit_status_code)  # return code of command run in remote host
```

* usage 3: run interactive command in remote host
  for if we want to run python3 in remote host ,then dive into >>> prompt, then run print(1+1) in python interactive
  shell,and then run exit() to back to linux shell. We can programming like following.

```python
from lambkid import SSHClient

ssh = SSHClient(ip="127.0.0.1", port=22, username="root", password="root@123")
cmd_prompt=[
        ["python3",">>>"],
        ["print(1+1)",">>>"],
        ["exit()","#"]
    ]
rs = ssh.exec_interactive(cmd_prompt)
print(rs.output)  # display of command run in remote host
print(rs.exit_status_code)  # return code of command run in remote host
```
rs.output may like following:
```bash
[root@redrose2100 ~]# python3
Python 3.6.8 (default, Apr  2 2020, 13:34:55) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
print(1+1)
2
>>> 
exit()
[root@redrose2100 ~]# 
```


* usage 4: copy file or dir from local to remote

```python
from lambkid import SSHClient

ssh = SSHClient(ip="127.0.0.1", port=22, username="root", password="root@123")
ssh.scp_to_remote("local/file/path/","remote/file/path")
```