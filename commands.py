import requests as req
from flask import request


def get_info(docker_engine):
    try:
        response = req.get(docker_engine + '/info').json()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_images_list(docker_engine):
    try:
        response = req.get(docker_engine + '/images/json').json()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_container_list(docker_engine):
    try:
        response = req.get(docker_engine + '/containers/json').json()
    except req.exceptions.ConnectionError:
        response = ""
    return response
