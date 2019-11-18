### Reproducing the connection failure between Python 3.7 and Kafka with SSL encryption

To reproduce the problem, follow these steps in a local terminal:

0. Optionally, pull the required Docker images before starting (takes a few minutes):
	- `docker pull jupyter/tensorflow-notebook:be289da10d60`
	- `docker pull jupyter/tensorflow-notebook:4d7dd95017ed`
	- `docker pull confluentinc/cp-kafka:5.3.1`
	- `docker pull confluentinc/cp-zookeeper:5.0.0`
1. `pwd path/to/repo/python-kafka-mre/` (further commands need to be run from this directory!)
2. `docker-compose -f mre-docker-compose36.yml up --abort-on-container-exit`
3. Wait 30 seconds; note that the python container prints the python and openssl versions it is using then successfully connects to Kafka (`DEBUG:pykafka.connection:Successfully connected to b'kafka':9092`), and exits with code 0
4. `docker-compose -f mre-docker-compose36.yml down`
5. `docker-compose -f mre-docker-compose37.yml up --abort-on-container-exit`
6. Wait 30 seconds; note that the python container prints the python and openssl versions it is using then produces errors (`INFO:pykafka.connection:[SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1056)`), does not connect to Kafka, and exits with non-zero exit code
7. `docker-compose -f mre-docker-compose37.yml down`

#### Other things I've tried:
- Use a different package to connect to Kafka (connection with `faust` produces basically the same error)
- Use a different cipher suite (and verify that setting them incompatibly changes the error to no cipher suites in common)
- Use a different version of the Kafka container (Confluent's Kafka 5.0.0 container with python 3.7 returns a `no cipher suites in common` error)
- Use a different protocol (enabling only TLS1.1 or 1.2 produces the same error, enabling 1.1 on Kafka and 1.2 on python or vice-versa causes a failure in name resoltion)
- Use a different version of openssl (this error was originally found using openssl 1.1.1c, and reproduced on 1.1.1a; for the current demonstration both containers use 1.1.1b)

NOTE: The credentials here are made explicitly for this purpose, and are not secure. Do not use them anywhere security might matter!
