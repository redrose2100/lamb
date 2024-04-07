# usage of log in lambkid

## install lambkid

details refer to [install lambkid](install.md)

## usage of log

* usage 1: Use log with default config
  In this case, log level default is logging.INFO, log path default is
  {path_of_python_in_your_machine}/Lib\site-packages/lambkid/lambkid_YYYYMMDD.log in windows and /var/log/lambkid/lambkid.log in
  linux or mac.

```python
from lambkid import log

log.info("test info log")
log.warning("test warning log")
log.error("test error log")
```

* usage 2: Customized your own log config
  In this case you can set log name, log level, and log path as following example.

```bash
import logging
from lambkid import get_logger

log=get_logger("myapp",logging.warning,"/home/myname/myapp/myapp.log")
```