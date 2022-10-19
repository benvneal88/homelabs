import docker
import logging

def get_docker_client():
    return docker.from_env()


def get_container_by_name(docker_client, container_name):
    for container in docker_client.list():
        if container.name == container_name:
            return container
        else:
            return None


def start_game_server(server_name):
    pass


def patch_game_server(server_name):
    pass


def restart_game_server(server_name):
    pass

