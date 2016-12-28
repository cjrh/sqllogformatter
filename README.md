# sqllogformatter

A Python logging Formatter subclass for messages with SQL queries

## Demo

```python
>>> import logging
>>> handler = logging.StreamHandler()
>>> from sqllogformatter import SQLLogFormatter
>>> formatter = SQLLogFormatter(fmt='%(asctime)s\n%(message)s\n')
>>> handler.setFormatter(formatter)
>>> logger = logging.getLogger('demo')
>>> logger.setLevel(logging.DEBUG)
>>> logger.addHandler(handler)
>>> logger.info(
    'select person.name as name, person.age as age, person.height as height, '
    'person.address as address from person where person.age > 30 and '
    'person.name like "cal%"')
2016-12-28 12:32:50,233

  File "/Users/.../ptpython", line 11, in <module>
    sys.exit(run())

  <...snip...>

  File "/Users/.../ptpython/repl.py", line 113, in _execute
    result = eval(code, self.get_globals(), self.get_locals())
  File "<stdin>", line 1, in <module>

SELECT person.name AS name,
       person.age AS age,
       person.height AS height,
       person.address AS address
FROM person
WHERE person.age > 30
  AND person.name LIKE "cal%"

>>>
```

Several things to notice:

0. The query has been formatted neatly enough to allow you to copy and paste it
into a DB tool for further analysis.
0. The stack frames are given _at the time the query was generated_. This means
that, for example, if you use **SQLAlchemy's** `DATABASE_ECHO=True` mode, you'll
get the locations in **your code** that generated each of the queries.

What you can't see above is that the query itself has been colorized:

![Colorized SQL Query](colorsql.png)


