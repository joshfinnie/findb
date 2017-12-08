import mock
import pytest
from datetime import datetime

import findb
from findb.exceptions import (
    DecrementNonInt, FileLoadError, FileWriteError, IncrementNonInt)

DB_SIZE = 3
MOCK_DATA = {'last_saved': 'now', 'data': {'test': 'foo'}}


@pytest.fixture
def db():
    db = findb.DB()
    db.set('key1', 'value1')
    db.set('key2', 'value2')
    db.set('fix_count', 100)
    yield db
    db.flushdb()


@mock.patch('findb.findb.FinDB._load')
def test_initialization_with_location(mock_load):
    findb.DB('fake.db')
    mock_load.assert_called_with()


def test__load_with_no_location(db):
    db._load()
    assert db.data == {}


@mock.patch('findb.findb.path.exists')
@mock.patch('findb.findb.open')
@mock.patch('findb.findb.load')
def test__load_with_location(mock_load, mock_open, mock_exists, db):
    location = 'fake.db'
    db.location = location
    mock_exists.return_value = True
    mock_load.return_value = MOCK_DATA
    db._load()
    mock_open.assert_called_with(location, 'rb')
    mock_exists.assert_called_with(location)
    assert db.last_saved == MOCK_DATA['last_saved']
    assert db.data == MOCK_DATA['data']
    db.location = None


@mock.patch('findb.findb.path.exists')
@mock.patch('findb.findb.open')
@mock.patch('findb.findb.load')
def test__load_failure_on_open(mock_load, mock_open, mock_exists, db):
    location = 'fake.db'
    db.location = location
    mock_exists.return_value = True
    mock_open.side_effect = Exception("fake exception")
    with pytest.raises(Exception):
        db._load()
    db.location = None


@mock.patch('findb.findb.path.exists')
@mock.patch('findb.findb.open')
@mock.patch('findb.findb.load')
def test__load_failure_on_load(mock_load, mock_open, mock_exists, db):
    location = 'fake.db'
    db.location = location
    mock_exists.return_value = True
    mock_load.side_effect = Exception("fake exception")
    with pytest.raises(FileLoadError):
        db._load()
        mock_open.assert_called_with(location, 'rb')
    db.location = None


@mock.patch('findb.findb.open')
@mock.patch('findb.findb.dump')
def test__save_with_location(mock_dump, mock_open, db):
    location = 'fake.db'
    mock_open_fs = mock.Mock()
    mock_open.return_value = mock_open_fs
    db.location = location
    db._save()
    mock_open.assert_called_with(location, 'wt')
    mock_dump.assert_called_with(db.__dict__, mock_open_fs, 2)
    db.location = None


@mock.patch('findb.findb.open')
@mock.patch('findb.findb.dump')
def test__save_failure_on_open(mock_dump, mock_open, db):
    location = 'fake.db'
    db.location = location
    mock_open.side_effect = Exception("fake exception")
    with pytest.raises(Exception):
        db._save()
    db.location = None


@mock.patch('findb.findb.open')
@mock.patch('findb.findb.dump')
def test__save_failure_on_dump(mock_dump, mock_open, db):
    location = 'fake.db'
    db.location = location
    mock_dump.side_effect = Exception("fake exception")
    with pytest.raises(FileWriteError):
        db._save()
        mock_open.assert_called_with(location, 'wt')
    db.location = None


def test_if_db_is_iterable(db):
    try:
        _ = (e for e in db)  # noqa: F841
    except TypeError:
        pytest.fail("Cannot iterate db")


def test_get_with_no_data(db):
    result = db.get('no_key')
    assert result is False


def test_get_with_real_key(db):
    result = db.get('key1')
    assert result == 'value1'


def test_incr_with_no_key(db):
    result = db.incr('count')
    assert result == 1


def test_incr_with_key(db):
    result = db.incr('fix_count')
    assert result == 101


def test_incr_with_non_int_key(db):
    with pytest.raises(IncrementNonInt):
        db.incr('key1')


def test_decr_with_no_key(db):
    result = db.decr('count')
    assert result == -1


def test_decr_with_key(db):
    result = db.decr('fix_count')
    assert result == 99


def test_decr_with_non_int_key(db):
    with pytest.raises(DecrementNonInt):
        db.decr('key1')


def test_lastsave(db):
    result = db.lastsave()
    assert result == datetime.fromtimestamp(db.last_saved)


def test_keys(db):
    result = db.keys()
    assert sorted(result) == sorted(['fix_count', 'key1', 'key2'])


def test_dbsize(db):
    result = db.dbsize()
    assert result == DB_SIZE


def test_set(db):
    result = db.set('aoeu', 'foo')
    assert result is True
    assert db.dbsize() == DB_SIZE + 1


def test_delete(db):
    result = db.delete('key2')
    assert result is True
    assert db.dbsize() == DB_SIZE - 1


def test_flushdb(db):
    result = db.flushdb()
    assert result is True
    assert db.dbsize() == 0


@mock.patch('findb.findb.remove')
def test_deletedb(mock_remove, db):
    location = 'fake.db'
    db.location = location
    db.deletedb()
    mock_remove.assert_called_with(location)
    db.location = None


def test_deletedb_with_no_location(db):
    mock_flushdb = mock.Mock()
    db.flushdb = mock_flushdb
    db.deletedb()
    mock_flushdb.assert_called_with()
