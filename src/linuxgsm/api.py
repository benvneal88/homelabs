import os
from unittest.mock import patch

import docker
import json
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


def copy_bytes_to_container(container, source_bytes_buffer, target_file_path):
    logger = get_logger()

    file_name = os.path.basename(target_file_path)
    logger.info(f"Copying bytes to container '{container.name}' to {target_file_path}")
    
    tar_bytes_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes_stream, mode='w|') as tar:
        info = tar.gettarinfo(fileobj=source_bytes_buffer)
        info.name = file_name
        logger.info(f"File name { os.path.basename(file_name)}")
        tar.addfile(info, source_bytes_buffer)

    container.put_archive(target_file_path, tar_bytes_stream.getvalue())


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

    server_patch_path = os.path.join(f"src/linuxgsm/{server_name}")

    if not os.path.exists(server_patch_path):
        logger.error(f"Server {server_name} not found ")
        #TODO: exit handling

    patch_config = json.load("src/linuxgsm/patch_config.json")

    for patch_file_dict in patch_config[server_name]:
            
            server_file_path = patch_file_dict['server_file_path'].replace("${server_name}", "server_name")
            source_file_path = patch_file_dict['source_file_path']

            with open(source_file_path, 'r') as file:
                transformed_file_buffer = file.read()

            if "find_replace_str" in patch_file_dict.keys():
                server_password = 'ttestt'
                for replace_str, with_str in patch_file_dict["find_replace_str"]:
                    transformed_file_buffer = transformed_file_buffer.replace(replace_str, with_str.replace("${server_password}", server_password))
        
            logger.info(f"Creating server file {server_file_path}")
            copy_bytes_to_container(container, transformed_file_buffer, server_file_path)
           


def start_game_server(server_name):
    pass


def restart_game_server(server_name):
    pass

