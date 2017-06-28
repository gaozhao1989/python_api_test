import logging,time
import pytest


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('BaseTest')
time.sleep(1)

class BaseTest(object):
    """Base Test for general tests.
    general setup and teardown func in bast_test
    """
    @classmethod
    @pytest.fixture(scope="session", autouse=True)
    def base_test(self):
        log.debug('set up test:')
        yield
        log.debug('tear down test:')
        time.sleep(1)