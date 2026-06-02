0. requirements 
    - docker
    - python env 
    - config/config.yml
        * topic
        * 

1. Mosquitto service
    - pull image 
        docker pull eclipse-mosquitto
    - create required folders
    - run the service : 
        $ docker run -d -p 1883:1883 -v "$PWD/src/data-ingestion/mosquitto/log:/mosquitto/log" -v "$PWD/src/data-ingestion/mosquitto/data:/mosquitto/data" eclipse-mosquitto

2. Publisher
    - simulate transactions
    - send data in the topic

3. Subscriber
    - listen to the topic
    - simple ETL (Casting data, add new column and validate data )
    - insert into a sqlite database

Resources :
- https://hub.docker.com/_/eclipse-mosquitto/
- https://pypi.org/project/paho-mqtt/