""" A logging formatter for SQL statements """


__version__ = '2016.12.2'
import logging
import inspect
import traceback
from itertools import cycle

import sqlparse
import termcolor


DEFAULT_OMISSIONS = (
    '/site-packages/sqlalchemy',
    'logging/__init__.py',
    '/site-packages/twisted/',
    '/threading.py',
    'frames = traceback.format_stack(inspect.currentframe())',
)


class SQLLogFormatter(logging.Formatter):
    """Pretty-print SQL statements and show where they were generated

    This custom formatter is intended for use with loggers that write out
    SQL queries. This formatter will:

    - nicely format the SQL queries to be much more readable
    - print each successive query in a different color
    - include stack information to show where the query was initiated
    - allow filtering out of the stack frames to reduce noise.

    """
    def __init__(self, fmt=None, datefmt=None,
                 colorcycle=('red', 'green', 'yellow', 'blue', 'magenta', 'cyan'),
                 incude_stack_info=True,
                 omit=DEFAULT_OMISSIONS):
        super(SQLLogFormatter, self).__init__(fmt, datefmt)
        self.colors = cycle(colorcycle)
        self.omit = omit

    def format(self, record):
        # type: (logging.LogRecord) -> str
        try:
            record.msg = sqlparse.format(record.msg, reindent=True, keyword_case='upper')
            if self.colors:
                record.msg = termcolor.colored(record.msg, next(self.colors))
            frames = traceback.format_stack(inspect.currentframe())
            stack = ''.join(f for f in frames if not any(_ in f for _ in self.omit))
            record.msg = '\n' + stack + '\n' + record.msg
        except:
            logging.exception()
        return super(SQLLogFormatter, self).format(record)
