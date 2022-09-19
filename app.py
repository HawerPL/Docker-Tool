import requests.exceptions
from flask import Flask
from flask import render_template
from flask import request
import json
import docker
import requests as req
import commands as cmd


app = Flask(__name__)

with open('appsettings.json', 'r') as file:
    config = json.load(file)

registry = config['registryAddresses'][0]['address']


@app.route('/')
def get_index():
    return render_template('index.html', name='index')


@app.route('/registry')
def get_registry_view():

    return render_template('registry.html', name='registryView', registry=registry)


@app.route('/management', methods=['GET', 'POST'])
def get_management_view():
    response = ""
    result = ""
    command = get_command()

    docker_engines = config['dockerHosts']
    docker_engine = request.args.get('docker_engine', type=str)
    if docker_engine:
        client = docker.DockerClient(base_url=docker_engine)

    if command == 'info':
        response = cmd.get_info(client)
    elif command == "containersList":
        if request.method == "POST":
            cmd.execute_container_operation(client, request.form.get('container-id'), request.form.get('operation'))
        response = cmd.get_container_list(client)
    elif command == "imagesList":
        response = cmd.get_images_list(client)
    elif command == "exec":
        response = cmd.get_container_list(client)
        if request.method == 'POST':
            result = cmd.execute_command(client, request.form.get('container-id'), request.form.get('command'))
    elif command == "volumesList":
        response = cmd.get_volumes_list(client)
    elif command == "networksList":
        response = cmd.get_networks_list(client)
    elif command == "pluginsList":
        response = cmd.get_plugins_list(client)
    return render_template('management.html', docker_engines=docker_engines, docker_engine=docker_engine, response=response,
                           result=result)


@app.template_global(name='get_repositories')
def get_repositories():
    try:
        response = req.get(registry + '/_catalog').json()['repositories']
    except req.exceptions.ConnectionError:
        response = ""
    return response


# @app.template_global(name='ping_docker_engines')
# def ping_docker_engines():
#     try:
#         #obecnie pinguje jeden serwer, ponieważ wsparcie tylko dla jednego serwera
#         response = req.get(dockerEngines + '_ping')
#     except req.exceptions.ConnectionError:
#         response = "NOK"
#     return response


@app.template_global(name='get_tags')
def get_tags():
    repository = request.args.get('repository', type=str)

    if repository is None:
        # return "Wybierz repozytorium w bocznym menu"
        return ""
    else:
        response = req.get(registry + '/' + repository + '/tags/list').json()
        return response['tags']


@app.template_global(name="get_command")
def get_command():
    command = request.args.get('command', type=str)
    if command is None:
        # return "Wybierz repozytorium w bocznym menu"
        return ""
    else:
        return command


@app.template_global(name="get_docker_engine")
def get_docker_engine():
    docker_engine = request.args.get('docker_engine', type=str)
    if docker_engine is None:
        return ""
    else:
        return docker_engine


if __name__ == '__main__':
    app.run()
