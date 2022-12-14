from flask import Flask, render_template, request
import json
import docker
import requests as req
import commands as cmd

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

with open('appsettings.json', 'r') as file:
    config = json.load(file)

# Global variables
registry_addr = config['registryAddresses'][0]['address']


@app.route('/')
def index():
    return render_template('index.html', name='index')


@app.route('/registry')
def registry():
    return render_template('registry.html', name='registryView', registry=registry_addr)


# TODO: Rozdzielić opcje zarządzania na nowe funkcje
@app.route('/management', methods=['GET', 'POST'])
@app.route('/management/<command>', methods=['GET', 'POST'])
def management(command=""):
    response = ""
    result = ""

    docker_engines = config['dockerHosts']
    docker_engine = request.args.get('docker_engine', type=str)
    if docker_engine:
        client = docker.DockerClient(base_url=docker_engine)

    if docker_engine:
        match command:
            case 'info':
                response = cmd.get_info(client)
            case 'containersList':
                if request.method == "POST":
                    cmd.execute_container_operation(client, request.form.get('container-id'),
                                                    request.form.get('operation'))
                response = cmd.get_container_list(client)
            case 'imagesList':
                response = cmd.get_images_list(client)
                if request.method == 'POST':
                    result = cmd.execute_image_operation(client, request.form.get('image-id'),
                                                         request.form.get('operation'))
            case 'exec':
                response = cmd.get_container_list(client)
                if request.method == 'POST':
                    result = cmd.execute_command(client, request.form.get('container-id'), request.form.get('command'))
            case 'volumesList':
                response = cmd.get_volumes_list(client)
                if request.method == 'POST':
                    result = cmd.execute_volume_operation(client, request.form.get('volume-id'),
                                                          request.form.get('operation'))
            case 'networksList':
                response = cmd.get_networks_list(client)
                if request.method == 'POST':
                    result = cmd.execute_network_operation(client, request.form.get('network-id'),
                                                           request.form.get('operation'))
            case 'pluginsList':
                response = cmd.get_plugins_list(client)

    return render_template('management.html', docker_engines=docker_engines, docker_engine=docker_engine,
                           response=response, result=result, command=command)


@app.template_global(name='get_repositories')
def get_repositories():
    try:
        response = req.get(registry_addr + '/_catalog').json()['repositories']
    except req.exceptions.ConnectionError:
        response = ""
    return response


def ping_docker_engines(docker_engines):
    try:
        for docker_engine in docker_engines:
            address = docker_engine['address']
            client = docker.DockerClient(base_url=address)
            response = client.ping()
    except req.exceptions.ConnectionError:
        response = "NOK"
    return response


@app.template_global(name='get_tags')
def get_tags():
    repository = request.args.get('repository', type=str)
    if repository is not None:
        response = req.get(registry_addr + '/' + repository + '/tags/list').json()
        return response['tags']
    else:
        return ""


@app.template_global(name="get_docker_engine")
def get_docker_engine():
    docker_engine = request.args.get('docker_engine', type=str)
    if docker_engine is None:
        return ""
    else:
        return docker_engine


@app.template_global(name="get_saved_commands")
def get_saved_commands():
    return config['commands']


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errorPage.html", error_code="404", error_message="Nie znaleziono strony"), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template("errorPage.html", error_code="500",
                           error_message="Wystąpił błąd po stronie serwera: " + str(error)), 500
