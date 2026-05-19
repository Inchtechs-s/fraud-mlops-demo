0. requirements 
    - docker
    - python env 

1. Run mosquitto service
    - pull image 
        docker pull eclipse-mosquitto:openssl
    - create required folders
    - edit the config file 
    - run the service : 
        $ docker run -d -p 1883:1883 -v "$PWD/src/data-ingestion/mosquitto/log:/mosquitto/log" -v "$PWD/src/data-ingestion/mosquitto/data:/mosquitto/data" eclipse-mosquitto


2. Run publisher
    - read data
    - create a topic 
    - send data

3. Run consummer
    - listen to the topic
    - simple ETL
    - store into sqlite 

Resources :
- https://hub.docker.com/_/eclipse-mosquitto/