#!/usr/bin/env python3

import argparse
import json
import urllib3

urllib3.disable_warnings()

__author__ = 'Dmytro Prokhorenkov'
__version__ = '0.4.0'

EXIT_STATUS = {
    0: "OK",
    1: "WARNING",
    2: "CRITICAL",
    3: "UNKNOWN"
}


def parse_args():
    argp = argparse.ArgumentParser(add_help=True,
                                   description='Check Pi-hole (version >=6.0.0) status',
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
    args = argp.parse_args()
    return args


def gtfo(exitcode, message=''):
    if message:
        print(''.join([EXIT_STATUS[exitcode], ":", " ", message]))
    exit(exitcode)


def check_pihole(host, port, auth, secure, _timeout, api):
    api_url = 'http' + ('s' if secure else '') + '://' + host + ('' if port == 80 else ":"+str(port)) + '/api/'
    api_headers = {'accept': 'application/json', 'sid': auth}
    try:
        cert_reqs = 'CERT_NONE' if secure else ''
        request = urllib3.PoolManager(cert_reqs=cert_reqs)
        content = request.request('GET', api_url + api, headers=api_headers, timeout=_timeout)
        decoded = json.loads(content.data.decode('utf8'))
        return 0, decoded
    except Exception:
        return 2, "Problems with accessing API: Check if server is running."


def main():
    args = parse_args()
    exitcode, url_output = check_pihole(args.host, args.port, args.auth, args.secure, args.timeout, 'dns/blocking')
    message = ""

    # Error handling statments
    if exitcode == 2:
        gtfo(2, url_output)
    if "error" in url_output:
        gtfo(2, "Connection Failed: " + url_output["error"]["message"])
    if url_output["blocking"] != "enabled":
        gtfo(1, "Pi-hole blocking is currently disabled")

    # Fetch Pi-hole Statistics
    exitcode, status_results = check_pihole(args.host, args.port, args.auth, args.secure, args.timeout, 'stats/summary')
    if exitcode == 2:
        gtfo(2, url_output)

    message = message + "Pi-hole is " + url_output["blocking"] + ": queries today - " + \
        str(status_results["queries"]["total"]) + ", domains blocked: " + str(status_results["queries"]["blocked"]) + \
        ", percentage blocked: " + str(status_results["queries"]["percent_blocked"]) + \
        "|queries=" + str(status_results["queries"]["total"]) + " blocked=" + str(status_results["queries"]["blocked"]) + " clients=" + str(status_results["clients"]["total"])

    # Exit with results
    gtfo(exitcode, message)


if __name__ == '__main__':
    main()
