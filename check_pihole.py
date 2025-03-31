#!/usr/bin/env python3

import argparse
import requests

__author__ = 'Dmytro Prokhorenkov'

EXIT_STATUS = {
    0: "OK",
    1: "WARNING",
    2: "CRITICAL",
    3: "UNKNOWN"
}


def parse_args():
    argp = argparse.ArgumentParser(add_help=True,
                                   description='Check Pi-hole (version >=6.0.0) status')
    argp.add_argument('-H', '--host', type=str, help="Pi-hole ip address or hostname", required=True)
    argp.add_argument('-P', '--port', type=int, help="Port number for Pi-Hole web UI", default=80)
    argp.add_argument('-A', '--auth', type=str, help="API Auth Key", required=True)
    argp.add_argument('-S', '--secure', help="Use ssl for connection", action='store_true')
    argp.add_argument('-C', '--critical', help="Forces CRITICAL when Pi-hole is disabled", action='store_true')
    argp.add_argument('-n', '--no-stats', help="Disable stats in output", action='store_true')
    argp.add_argument('-t', '--timeout', default=10, type=int, help='Timeout for request. Default 10 seconds')
    args = argp.parse_args()
    return args


def gtfo(exitcode, message=''):
    if message:
        print(''.join([EXIT_STATUS[exitcode], ":", " ", message]))
    exit(exitcode)


def generate_url(host, port, secure):
    return f"{'https' if secure else 'http'}://{host}:{port}/api"


def pihole_get_sid(url, auth, secure, timeout) -> tuple[str, str]:
    _url = '/'.join([url, 'auth'])
    payload = {"password": auth}
    try:
        response = requests.request('POST', _url, json=payload, verify=False, timeout=timeout)
        valid = response.json()['session']['valid']
        if not valid:
            return 2, "Problems with accessing API: Check if provided password is correct."

        sid = response.json()['session']['sid']
        return sid, ""

    except Exception as e:
        print(e)
        return "", "Problems with accessing API: Check if server is running."

def pihole_logout(url, sid, secure, timeout) -> bool:
    payload = {}
    headers = {
      "X-FTL-SID": sid
    }
    _url = '/'.join([url, 'auth'])
    try:
        response = requests.request('DELETE', _url, data=payload, headers=headers, verify=False, timeout=timeout)
        return True
    except Exception as e:
        return False


def pihole_get_info(url, sid, secure, timeout, api_endpoint) -> tuple[int, str]:
    api_headers = {'accept': 'application/json', 'sid': sid}
    _url = '/'.join([url, api_endpoint])
    try:
        response = requests.request('GET', _url, headers=api_headers, timeout=timeout)
        decoded = response.json()
        return 0, decoded
    except Exception:
        return 2, "Problems with accessing API: Check if server is running."


def main():
    args = parse_args()

    url = generate_url(args.host, args.port, args.secure)

    sid, err = pihole_get_sid(url, args.auth, args.secure, args.timeout)
    if sid == "":
        gtfo(2, err)

    exitcode, url_output = pihole_get_info(url, sid, args.secure, args.timeout, 'dns/blocking')

    # Error handling statments
    if exitcode == 2:
        gtfo(2, url_output)
    if "error" in url_output:
        gtfo(2, "Connection Failed: " + url_output["error"]["message"])
    if url_output["blocking"] != "enabled":
        blocking_exitcode = 1
        if args.critical:
            blocking_exitcode = 2
        gtfo(blocking_exitcode, "Pi-hole blocking is currently disabled")

    if args.no_stats:
        message = ' '.join(["Pi-hole is", url_output["blocking"]])
    else:
        # Fetch Pi-hole Statistics
        exitcode, status_results = pihole_get_info(url, sid, args.secure, args.timeout, 'stats/summary')
        if exitcode == 2:
            gtfo(2, url_output)
        message = "Pi-hole is " + url_output["blocking"] + ": queries today - " + \
            str(status_results["queries"]["total"]) + ", domains blocked: " + str(status_results["queries"]["blocked"]) + \
            ", percentage blocked: " + str(status_results["queries"]["percent_blocked"]) + \
            "|queries=" + str(status_results["queries"]["total"]) + " blocked=" + \
            str(status_results["queries"]["blocked"]) + " clients=" + str(status_results["clients"]["total"])

    pihole_logout(url, sid, args.secure, args.timeout)

    # Exit with results
    gtfo(exitcode, message)


if __name__ == '__main__':
    main()
