import os

import docker
import logging
import tarfile


def get_logger():
    return logging.getLogger(__name__)


def get_docker_client():
    return docker.from_env()


def patch_game_server(server_name):
    """
    Copies server files to game server and restarts the server

    """
    client = get_docker_client()
    container = client.containers.get(server_name)
    logger = get_logger()
    
    server_patch_path = os.getcwd(), server_name
    logger.info(f"Server patch path: {server_patch_path}")
    if not os.path.exists(os.path.join()):
        logger.error(f"Server {server_name} not found ")

    os.chdir(server_patch_path)
    # srcname = os.path.basename(src)
    # tar = tarfile.open(src + '.tar', mode='w')
    # try:
    #     tar.add(srcname)
    # finally:
    #     tar.close()

    # data = open(src + '.tar', 'rb').read()
    # container.put_archive(os.path.dirname(dst), data)
    
    # return container


def start_game_server(server_name):
    pass


def restart_game_server(server_name):
    pass

