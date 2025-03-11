# icinga2_check_pihole

Icinga2/Nagios plugin to check Pi-hole status.

```bash
usage: check_pihole.py [-h] -H HOST [-P PORT] [-A API_KEY] [-S] [-C] [-W] [-t TIMEOUT]

Check Pi-hole status

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Pi-hole ip address or hostname
  -T TOKEN, --token TOKEN Pi-hole api token
  -P PORT, --port PORT  Port number for Pi-Hole web UI
  -A API_KEY, --auth API_KEY  API 
                        Token for backend access
  -S, --secure          Use ssl for API access
  -C, --status_critical
                        Forces CRITICAL when Pi-hole is disabled
  -W, --status_warning  Forces WARNING when Pi-hole is disabled
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for request. Default 10 seconds

check_pihole.py: v.0.2.1 by Dmytro Prokhorenkov
```
