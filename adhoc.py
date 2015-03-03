"""Ad-hoc JIRA query script.

Install with:

    $ virtualenv --no-site-packages jira-adhoc
    $ cd jira-analysis
    $ ./bin/pip install jira

Modify adhoc.py (this file) and change the `process()` function to perform
whatever analysis is required using the JIRA API client.

Run with:

    $ ./bin/python adhoc.py https://jirainstance.jira.net
"""

from __future__ import print_function

import getpass
import argparse
import pprint

from jira import JIRA

def connect(url):
    print("Connecting to ", url)
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")

    options = {
        'server': url
    }

    return JIRA(options, basic_auth=(username, password,))

def main():

    parser = argparse.ArgumentParser(description='Ad-hoc JIRA queries')
    parser.add_argument('url', metavar='https://acme.jira.com', help='URL to JIRA instance')

    args = parser.parse_args()

    jira = connect(args.url)

    process(jira, args)

def process(jira, args):
    """Put code here. See http://jira.readthedocs.org/en/latest/
    """

    print()

    query = """
        issuetype = "Feature"
    AND resolution is EMPTY
    """

    issues = jira.search_issues(query)

    for i in issues:
        print("* [%s](%s/browse/%s) - %s" % (
            i.key,
            args.url, i.key,
            i.fields.summary
        ))

        for link in i.fields.issuelinks:
            linkedIssue = getattr(link, 'inwardIssue', getattr(link, 'outwardIssue', None))
            if linkedIssue is not None and linkedIssue.fields.issuetype.name == "Dependency":
                # Get rest of fields
                linkedIssue = jira.issue(linkedIssue.key)
                if linkedIssue.fields.resolution is None:
                    print("    * [%s](%s/browse/%s)\t%s - %s" % (
                        linkedIssue.key,
                        args.url, linkedIssue.key,
                        linkedIssue.fields.duedate,
                        linkedIssue.fields.summary,
                    ))

        print()

if __name__ == '__main__':
    main()
