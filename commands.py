import requests as req


def get_info(docker_client):
    try:
        response = docker_client.info()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_images_list(docker_client):
    try:
        response = docker_client.images.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_container_list(docker_client):
    try:
        response = docker_client.containers.list(all=True)
    except req.exceptions.ConnectionError:
        response = ""
    return response


def execute_command(docker_client, container_id, command):
    try:
        container = docker_client.containers.get(container_id)
        response = container.exec_run(command)
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_volumes_list(docker_client):
    try:
        response = docker_client.volumes.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_networks_list(docker_client):
    try:
        response = docker_client.networks.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def get_plugins_list(docker_client):
    try:
        response = docker_client.plugins.list()
    except req.exceptions.ConnectionError:
        response = ""
    return response


def execute_container_operation(docker_client, container_id, operation):
    try:
        container = docker_client.containers.get(container_id)
        if operation == "start":
            container.start()
        elif operation == "restart":
            container.restart()
        elif operation == "pause":
            container.pause()
        elif operation == "unpause":
            container.unpause()
        elif operation == "update":
            container.update()
        elif operation == "stop":
            container.stop()
        elif operation == "remove":
            container.remove()
        response = "OK"
    except req.exceptions.ConnectionError:
        response = ""
    return response


def execute_image_operation(docker_client, image_id, operation):
    try:
        image = docker_client.images.get(image_id)
        if operation == "remove":
            image.remove()
            response = "OK"
    except req.exceptions.ConnectionError:
        response = ""
    return response


def execute_network_operation(docker_client, network_id, operation):
    try:
        network = docker_client.networks.get(network_id)
        if operation == "remove":
            network.remove()
            response = "OK"
    except req.exceptions.ConnectionError:
        response = ""
    return response

