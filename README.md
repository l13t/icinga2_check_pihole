# icinga2_check_pihole
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_pihole.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_pihole?ref=badge_shield)


Icinga2/Nagios plugin to check Pi-hole status.

```bash
usage: check_pihole.py [-h] -H HOST [-P PORT] [-C] [-W] [-t TIMEOUT]

Check Pi-hole status

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Pi-hole ip address or hostname
  -P PORT, --port PORT  Port number for Pi-Hole web UI
  -C, --status_critical
                        Forces CRITICAL when Pi-hole is disabled
  -W, --status_warning  Forces WARNING when Pi-hole is disabled
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for request. Default 10 seconds

check_pihole.py: v.0.2.1 by Dmytro Prokhorenkov
```


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_pihole.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_pihole?ref=badge_large)