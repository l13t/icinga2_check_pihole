# icinga2_check_pihole

Icinga2/Nagios plugin to check Pi-hole status.

```bash
usage: check_pihole.py [-h] [-H HOST] [-C] [-W] [-t TIMEOUT]

Check Pi-hole status

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Pi-hole ip address or hostname
  -C, --status_critical
                        Forces CRITICAL when Pi-hole is disabled
  -W, --status_warning  Forces WARNING when Pi-hole is disabled
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for request. Default 10 seconds

check_pihole.py: v.0.1.2 by Dmytro Prokhorenkov
```
