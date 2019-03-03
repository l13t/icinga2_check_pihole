#!/usr/bin/env python3

import sys, urllib3, base64, re, argparse, json

__author__ = 'Dmytro Prokhorenkov'
__version__= '0.1.1'

def parse_args():
    argp = argparse.ArgumentParser(add_help=True, description='Check for OOM killer events', epilog='{0}: v.{1} by {2}'.format('check_pihole.py', __version__, __author__))
    argp.add_argument('-H', '--host', type=str, help="PiHole ip address or hostname")
    argp.add_argument('-t', '--timeout', default=10, type=int, help='Timeout for request. Default 10 seconds')
    args = argp.parse_args()
    if (args.host == None):
        argp.print_help()
        sys.exit(0)
    return args

def gtfo(exitcode, message=''):
    if message:
        print(message)
    exit(exitcode)

def check_pihole(host, _timeout):
    status_url = 'http://' + host + '/admin/api.php?summaryRaw'
    try:
        request = urllib3.PoolManager()
        content  = request.request('GET', status_url, timeout=_timeout)
        decoded  = json.loads(content.data)
        return 0, decoded
    except Exception:
        return 2, "Problems with accessing API: Check if server is running."

def main():
    args = parse_args()
    exitcode, url_output = check_pihole(args.host, args.timeout)
    message = "OK: "
    if url_output["status"] != "enabled":
        message = "WARNING: "
    message = message + "PiHole is " + url_output["status"] + ": queries today - " + str(url_output["dns_queries_all_types"]) + ", domains blocked: " + str(url_output["ads_blocked_today"]) + ", percentage blocked: " + str(url_output["ads_percentage_today"])
    gtfo(exitcode, message)

if __name__ == '__main__':
    main()