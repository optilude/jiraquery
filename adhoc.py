from __future__ import print_function

import getpass
import argparse

from jira import JIRA

def connect(url):
    print("Connecting to ", url)
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")

    options = {
        'server': url
    }

    return JIRA(options, basic_auth=(username, password,))

def main(fn, args=()):
    """Connect to JIRA and call `fn()` as a callback with `jira` and `args`
    as arugments.
    """

    parser = argparse.ArgumentParser(description='Ad-hoc JIRA queries')
    parser.add_argument('url', metavar='https://acme.jira.com', help='URL to JIRA instance')

    for arg in args:
        parser.add_argument(arg)

    args = parser.parse_args()

    jira = connect(args.url)

    fn(jira, args)
