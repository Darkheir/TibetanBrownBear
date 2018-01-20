import pytest

from yeti.common.config import yeti_config
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

# pylint: disable=C0413
from yeti.core.model.arango import db
from yeti.core.types.observable import Observable
from yeti.core.types.hostname import Hostname

# Make sure we are not deleting the user's database when running tests

@pytest.fixture
def clean_db():
    # pylint: disable=W0212
    # We need to access the collections to make sure they are in the cache
    Observable._get_collection()
    Hostname._get_collection()
    db.clear()


@pytest.fixture
def populated_db():
    db.clear()
    for num in range(10):
        # We need to control the keys with which objects are created
        # pylint: disable=W0212
        Observable._get_collection().insert({
            'value': 'asd{0:d}'.format(num),
            '_key': str(num),
        })
        Hostname._get_collection().insert({
            'value': 'asd{0:d}.com'.format(num),
            '_key': str(num),
            'tld': 'com',
            'idna': 'asd{0:d}.com'.format(num),
        })
