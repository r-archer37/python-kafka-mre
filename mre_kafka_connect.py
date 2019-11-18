from time import sleep
from sys import version, stdout
from ssl import OPENSSL_VERSION

SLEEP_TIMER = 30

print(f'Python kernel sleeping {str(SLEEP_TIMER)} seconds.')
stdout.flush()
sleep(SLEEP_TIMER)

print('Python kernel has woken up.')


lineblock = '========================================================================'
message = [
    'This container is running Python version:',
    version,
    'with OpenSSL version:',
    OPENSSL_VERSION
]

print('\n'.join([lineblock]*3+message+[lineblock]*3))

sleep(1)

stdout.flush()

sleep(1)

import logging
import os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

KAFKA_ADDRESS = 'kafka:9092' # Probably 'kafka:9092' or 'kafka:9093'
SSL_PATH = 'mre.pem' # if not using, change to None

from pykafka import KafkaClient, SslConfig; import pykafka

if SSL_PATH is not None:
    ssl_config = SslConfig (
        cafile=SSL_PATH,
        certfile=SSL_PATH,
        keyfile=SSL_PATH,
    )
else:
    ssl_config = None
    
client = KafkaClient(KAFKA_ADDRESS,ssl_config=ssl_config)