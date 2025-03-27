# icinga2_check_pihole

Icinga2/Nagios plugin to check Pi-hole status.

```bash
usage: check_pihole.py [-h] -H HOST [-P PORT] -A AUTH [-S] [-C] [-W] [-t TIMEOUT]

Check Pi-hole (version >=6.0.0) status

options:
  -h, --help            show this help message and exit
  -H, --host HOST       Pi-hole ip address or hostname
  -P, --port PORT       Port number for Pi-Hole web UI
  -A, --auth AUTH       API Auth Key
  -S, --secure          Use ssl for connection
  -C, --status_critical
                        Forces CRITICAL when Pi-hole is disabled
  -W, --status_warning  Forces WARNING when Pi-hole is disabled
  -t, --timeout TIMEOUT
                        Timeout for request. Default 10 seconds
```
