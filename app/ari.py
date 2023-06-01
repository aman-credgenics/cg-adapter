import time

from contextlib import contextmanager
from app.exceptions import ARIConnectionException
from app.logging import AppLogger
from app.utils import SingletonMeta

import ari
import requests

logger = AppLogger.__call__().get_logger()

def asterisk_is_loading(error):
    #service unavailable
    if error.response.status_code==503:
        return True
    
    #not found
    elif error.response.status_code==404:
        return True
    
    #any other server error
    return False


class ARIClient(metaclass=SingletonMeta):
    _apps = []
    _is_running = False
    client = None

    def __init__(self, config):
        self.client = self.create_ari_client(config['connection'], config['startup_connection_tries'], config['startup_connection_delay'])
        self._apps = config['apps'].split(",")

    def _new_ari_client(self, ari_config, startup_connection_tries, startup_connection_delay):
        for _ in range(startup_connection_tries):
            try:
                return ari.connect(**ari_config)
            except requests.ConnectionError:
                logger.info('No ARI server found, retrying in %s seconds...', startup_connection_delay)
                time.sleep(startup_connection_delay)
                continue
            except requests.HTTPError as e:
                if asterisk_is_loading(e):
                    logger.info('ARI is not ready yet, retrying in %s seconds...', startup_connection_delay)
                    time.sleep(startup_connection_delay)
                    continue
                else:
                    raise ARIConnectionException
        raise ARIConnectionException
    
    @contextmanager
    def _running(self):
        self._is_running = True
        try:
            yield
        finally:
            self._is_running = False

    
    def connect(self):
        logger.debug('ARI client listening...')
        try:
            with self._running():
                self.client.run(apps=self._apps)
            self.client.close()
        except Exception as e:
            raise ARIConnectionException

    def stop(self):
        self._sync()
        try:
            self.client.close()
        except RuntimeError:
            pass
    
    def _sync(self):
        '''self.sync() should be called before calling self.stop(), in case the
        ari client does not have the websocket yet'''

        while self._is_running and not self.client.websockets:
            time.sleep(0.1)