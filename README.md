# FinDB

FinDB is a key-value store written in Python. Probably shouldn't use it for anything...


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
