# Homelabs 

Homelabs is a repo containing setup instructions and building automation operate the @paulie homelabs server

These instructions will configure a fresh linux install and enable the homelabs features


## Game Server

@Paulie Homelabs can run any linuxgsm supported game. 
https://linuxgsm.com/

Each game server will get have container service deployed.

Currently, two games are fully configured. 

- Valheim
- Project Zomboid 

Server settings for each game can be set in `src/linuxgsm/ci/..` and the files will get copied when the Docker image is built
