import requests.exceptions
from flask import Flask
from flask import render_template
from flask import request
import os
import requests as req
import commands as cmd

app = Flask(__name__)
registry = os.getenv('REGISTRY_ADDRESS')
dockerEngines = os.getenv('DOCKER_ENGINE_ADDRESS')


@app.route('/')
def get_index():
    return render_template('index.html', name='index')


@app.route('/registry')
def get_registry_view():
    return render_template('registryView.html', name='registryView', registry=registry)


@app.route('/management')
def get_management_view():
    response = ""
    command = get_command()
    docker_engine = get_docker_engine()
    if command == 'info':
        response = cmd.get_info(docker_engine)
    elif command == "containerList":
        response = cmd.get_container_list(docker_engine)
    elif command == "imagesList":
        response = cmd.get_images_list(docker_engine)
    elif command == "exec":
        response = "res"
    elif command == "volumesList":
        response = "res"
    elif command == "networkList":
        response = "res"
    return render_template('managementView.html', name='managementView', dockerEngines=dockerEngines, response=response)


@app.template_global(name='get_repositories')
def get_repositories():
    try:
        response = req.get(registry + '/_catalog').json()['repositories']
    except req.exceptions.ConnectionError:
        response = ""
    return response


@app.template_global(name='get_docker_engines')
def get_docker_engines():
    return [dockerEngines]


@app.template_global(name='ping_docker_engines')
def ping_docker_engines():
    try:
        #obecnie pinguje jeden serwer, ponieważ wsparcie tylko dla jednego serwera
        response = req.get(dockerEngines + '_ping')
    except req.exceptions.ConnectionError:
        response = "NOK"
    return response


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
