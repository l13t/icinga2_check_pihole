# icinga2_check_pihole

## About

Icinga2/Nagios plugin to check Pi-hole status. At the moment script supports only version 6.0.0 and above.

## Dependencies

- Python 3.9+
- Requests library

## How to use

```bash
usage: check_pihole.py [-h] -H HOST [-P PORT] -A AUTH [-S] [-C] [-n] [-t TIMEOUT]

Check Pi-hole (version >=6.0.0) status

options:
  -h, --help            show this help message and exit
  -H, --host HOST       Pi-hole ip address or hostname
  -P, --port PORT       Port number for Pi-Hole web UI
  -A, --auth AUTH       API Auth Key
  -S, --secure          Use ssl for connection
  -C, --critical        Forces CRITICAL when Pi-hole is disabled
  -n, --no-stats        Disable stats in output
  -t, --timeout TIMEOUT
                        Timeout for request. Default 10 seconds
```
