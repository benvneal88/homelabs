import os

import docker
import logging
import tarfile
import re


def get_logger():
    return logging.getLogger(__name__)


def get_docker_client():
    return docker.from_env()


def patch_game_server(server_name):
    """
    Copies server files to game server and restarts the server

    """
    #client = get_docker_client()
    #container = client.containers.get(server_name)
    logger = get_logger()
    
    server_patch_path = os.path.join(os.getcwd(), server_name)
    logger.info(f"Server patch path: {server_patch_path}")
    if os.path.exists(server_patch_path):
        os.chdir(server_patch_path)

        if server_name == 'pzserver':
            source_file_path = os.path.join(server_patch_path, 'pzserver.txt')
            transformed_file_path = os.path.join(server_patch_path, 'pzserver.ini')

            with open(source_file_path, 'r') as file:
                source_file_buffer = file.read()
                transformed_file_buffer = source_file_buffer.replace("PZ_SERVER_PASSWORD", )
                #print(source_file_buffer)

            # with tarfile.open(server_patch_path + '.tar', mode='w') as tar:
            #     try:
            #         tar.add(srcname)
            #     finally:
            #         tar.close()

    else:
        logger.error(f"Server {server_name} not found ")

        # srcname = os.path.basename(src)
        # tar = tarfile.open(src + '.tar', mode='w')


        # data = open(src + '.tar', 'rb').read()
        # container.put_archive(os.path.dirname(dst), data)
        
        # return container


def start_game_server(server_name):
    pass


def restart_game_server(server_name):
    pass

