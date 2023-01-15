#!/usr/bin/env python3

import argparse
import json

import urllib3
urllib3.disable_warnings()

__author__ = 'Dmytro Prokhorenkov'
__version__ = '0.3.0'

EXIT_STATUS = {
    0: "OK",
    1: "WARNING",
    2: "CRITICAL",
    3: "UNKNOWN"
}


def parse_args():
    argp = argparse.ArgumentParser(add_help=True,
                                   description='Check Pi-hole status',
                                   epilog='{0}: v.{1} by {2}'.format('check_pihole.py', __version__, __author__))
    argp.add_argument('-H', '--host', type=str, help="Pi-hole ip address or hostname", required=True)
    argp.add_argument('-P', '--port', type=int, help="Port number for Pi-Hole web UI", default=80)
    argp.add_argument('-A', '--auth', type=str, help="API Auth Key", required=True)
    argp.add_argument('-S', '--secure', help="Use ssl for connection", action='store_true')
    argp.add_argument('-C', '--status_critical', dest='pihole_status',
                      help="Forces CRITICAL when Pi-hole is disabled", action='store_true')
    argp.add_argument('-W', '--status_warning', dest='pihole_status',
                      help="Forces WARNING when Pi-hole is disabled", action='store_false')
    argp.add_argument('-t', '--timeout', default=10, type=int, help='Timeout for request. Default 10 seconds')
    argp.set_defaults(pihole_status=False)
    args = argp.parse_args()
    return args


def gtfo(exitcode, message=''):
    if message:
        print(''.join([EXIT_STATUS[exitcode], ":", " ", message]))
    exit(exitcode)


def check_pihole(host, port, auth, secure, _timeout):
    status_url = 'http' + ('s' if secure else '') + '://' + host + ('' if port == 80 else ":"+str(port)) + '/admin/api.php?summaryRaw&auth=' + auth
    try:
        cert_reqs = 'CERT_NONE' if secure else ''
        request = urllib3.PoolManager(cert_reqs=cert_reqs)
        content = request.request('GET', status_url, timeout=_timeout)
        decoded = json.loads(content.data.decode('utf8'))
        return 0, decoded
    except Exception:
        return 2, "Problems with accessing API: Check if server is running."


def main():
    args = parse_args()
    exitcode, url_output = check_pihole(args.host, args.port, args.auth, args.secure, args.timeout)
    message = ""
    if exitcode == 2:
        message = url_output
    else:
        if url_output["status"] != "enabled":
            if args.pihole_status:
                exitcode = 2
            else:
                exitcode = 1
        message = message + "Pi-hole is " + url_output["status"] + ": queries today - " + \
            str(url_output["dns_queries_all_types"]) + ", domains blocked: " + str(url_output["ads_blocked_today"]) + \
            ", percentage blocked: " + str(url_output["ads_percentage_today"]) + \
            "|queries=" + str(url_output["dns_queries_all_types"]) + " blocked=" + str(url_output["ads_blocked_today"]) + " clients=" + str(url_output['unique_clients'])
    gtfo(exitcode, message)


if __name__ == '__main__':
    main()
