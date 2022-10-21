import os

import docker
import logging
import tarfile
import re
import io

def get_logger(level='INFO'):
    logger =  logging.getLogger(__name__)

    if level.lower() == 'info':
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
        
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

    return logger


def get_docker_client():
    return docker.from_env()


def copy_file_to_container(container, source_file_path, target_dir_path):
    logger = get_logger()

    file_name = os.path.basename(source_file_path)
    logger.info(f"Copying file {source_file_path} to container '{container.name}' to {target_dir_path}")
    
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w|') as tar, open(source_file_path, 'rb') as f:
        info = tar.gettarinfo(fileobj=f)
        info.name = os.path.basename(source_file_path)
        tar.addfile(info, f)

    container.put_archive(target_dir_path, stream.getvalue())


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
    
    logger = get_logger()
    
    docker_client = get_docker_client()
    container = docker_client.containers.get(server_name)

    server_patch_path = os.path.join(os.getcwd(), 'src', 'linuxgsm', server_name)
    logger.info(f"Server patch path: {server_patch_path}")
    if os.path.exists(server_patch_path):
        os.chdir(server_patch_path)

        if server_name == 'pzserver':
            source_file_path = os.path.join(server_patch_path, 'pzserver.txt')
            transformed_file_path = os.path.join(server_patch_path, 'pzserver.ini')

            with open(source_file_path, 'r') as file:
                source_file_buffer = file.read()
                transformed_file_buffer = source_file_buffer.replace("PZ_SERVER_PASSWORD", "test")
            
            logger.info(f"Creating server file {transformed_file_path}")
            with open(transformed_file_path, 'w') as file:
                file.write(transformed_file_buffer)

            copy_file_to_container(container, transformed_file_path, "")

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

