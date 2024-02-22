# Example package with a console entry point
from . import time
from . import heartbeat

__all__ = ["time", "heartbeat"]


def main():
    print(
        """
===========================================================================
                      Dynamic Heartbeat by Hobee Liu
===========================================================================

Welcome to the dynamic_heartbeat package!
This package is designed to provide a dynamic heartbeat for a system.

just use the following command to get started:

```Python
import time
from dynamic_heartbeat import heartbeat as dhb

interval = dhb.Timer(default=10, min_=1, max_=60)
time.sleep(interval(True))  # True to slow down the heartbeat. 5s -> 10s
time.sleep(interval(False))  # False to speed up the heartbeat. 5s -> 2.5s
```

"""
    )
