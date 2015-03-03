# Ad-hoc JIRA query template

Install with:

    $ git clone https://github.com/optilude/jiraquery.git
    $ cd jiraquery
    $ virtualenv --no-site-packages .
    $ ./bin/pip install jira
    $ ./bin/pip install ipython

Create a file like `myanalysis.py`:

    import adhoc

    def process(jira, args):

        # put code here

    if __name__ == '__main__':
        adhoc.main(process, args=())

The code in `process()` can use `jira` as a JIRA API client. See
<http://jira.readthedocs.org/en/latest/> for details.

If you require additional command line arguments, pass them into the
`args` list, e.g. `args=('issuekey',)` (note trailing comma). These will
then be available as attributes of the `args` object.

Run with:

    $ ./bin/python myanalysis.py https://jirainstance.jira.net
