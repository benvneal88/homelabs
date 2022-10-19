import os

import docker
import logging
import tarfile
import re


def get_logger():
    return logging.getLogger(__name__)


def get_docker_client():
    return docker.from_env()


def copy_file_to_container(container, source_file_path, target_file_path):
    logger = get_logger()

    logger.info(f"Reading file {source_file_path}")
    with open(source_file_path, 'r') as file:
        file_data = file.read()

    file_name = os.path.basename(source_file_path)
    logger.info(f"Converting to tar file {file_name + '.tar'}")
    with tarfile.open(file_name + '.tar', mode='w') as tar:
        tar.add(file_data)

    data = open(file_name + '.tar', 'rb').read()
    logger.info(f"Tar data {data}")

    logger.info(f"Saving file {os.path.dirname(target_file_path)} to container {container.name}")
    container.put_archive(os.path.dirname(target_file_path), data)


def copy_file_from_container(container, source_file_path, target_file_path):
    logger = get_logger()
   
    logger.info(f"Copying file {source_file_path} from container {container.name}")
    tarfile = container.from_archive(source_file_path)
    with tarfile.open(tarfile, mode='r') as tar:
        file_data = tar.extract()

    logger.info(f"Saving file to {target_file_path}")
    with open(target_file_path, 'w') as file:
        file = file_data.write()

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

