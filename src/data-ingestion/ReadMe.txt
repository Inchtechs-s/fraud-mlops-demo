0. requirements 
    - docker
    - python env 

1. Run mosquitto service
    - pull image 
    - create required folders
    - edit the config file 
    - run the service

2. Run producer
    - read data
    - create a topic 
    - send data

3. Run consummer
    - listen to the topic
    - simple ETL
    - store into sqlite 

Resources :
- https://hub.docker.com/_/eclipse-mosquitto/