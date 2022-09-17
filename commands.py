import requests as req
import docker
from flask import request

client = docker.from_env()


def get_info(docker_engine):
    try:
        response = client.info()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_images_list(docker_engine):
    try:
        response = client.images.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_container_list(docker_engine):
    try:
        response = client.containers.list(all=True)
    except req.exceptions.ConnectionError:
        response = ""
    return response


def execute_command(docker_engine, container_id, command):
    try:
        container = client.containers.get(container_id)
        response = container.exec_run(command)
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_volumes_list(docker_engine):
    try:
        response = client.volumes.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_networks_list(docker_engine):
    try:
        response = client.networks.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_plugins_list(docker_engine):
    try:
        response = client.plugins.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response

