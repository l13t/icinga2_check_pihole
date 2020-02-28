#!/usr/bin/env python2

import sys, urllib3, base64, re, argparse, json

__author__ = 'Dmytro Prokhorenkov'
__version__= '0.1.2'

def parse_args():
    argp = argparse.ArgumentParser(add_help=True, description='Check Pi-hole status', epilog='{0}: v.{1} by {2}'.format('check_pihole.py', __version__, __author__))
    argp.add_argument('-H', '--host', type=str, help="Pi-hole ip address or hostname")
    argp.add_argument('-C', '--status_critical', dest='pihole_status', help="Forces CRITICAL when Pi-hole is disabled", action='store_true')
    argp.add_argument('-W', '--status_warning', dest='pihole_status', help="Forces WARNING when Pi-hole is disabled", action='store_false')
    argp.add_argument('-t', '--timeout', default=10, type=int, help='Timeout for request. Default 10 seconds')
    argp.set_defaults(pihole_status=False)
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
        if args.pihole_status == True:
            message = "CRITICAL: "
        else:
            message = "WARNING: "
    message = message + "Pi-hole is " + url_output["status"] + ": queries today - " + str(url_output["dns_queries_all_types"]) + ", domains blocked: " + str(url_output["ads_blocked_today"]) + ", percentage blocked: " + str(url_output["ads_percentage_today"]) + "|queries=" + str(url_output["dns_queries_all_types"]) +" blocked=" +  str(url_output["ads_blocked_today"])
    gtfo(exitcode, message)

if __name__ == '__main__':
    main()
