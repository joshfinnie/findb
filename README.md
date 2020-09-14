# FinDB

[![Test](https://github.com/joshfinnie/findb/workflows/Test/badge.svg)](https://github.com/joshfinnie/findb/actions?query=workflow%3ATest)

FinDB is a key-value store written in Python 3. Probably shouldn't use it for anything...


## Install

```
pip install -e .
```

## Use

```
import findb
db = findb.DB('test.db')
db.set('aoeu', 'foo')
db.get('aoeu')
```

## Tests

First, install the packages required for testing FinDB, then run the `make test` command.

```
$ pip install -r test-requirements.txt
$ make test
```

or if you have access to Docker run `make dtest` which will build a Docker container and run the tests on that container.
