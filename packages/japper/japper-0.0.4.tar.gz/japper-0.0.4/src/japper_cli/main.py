import argparse
import os, subprocess

from .init_project import init_project
from .globals import snake, run_command, print_console, save_config, load_config, get_input, add_page

WORKING_DIR = os.getcwd().replace('\\', '/')


def build_docker_image(dest, quiet=False):
    print_console('Building the Docker image...')
    cmd = f'cd container/{dest} && docker-compose build'
    if quiet:
        cmd += ' -q'
    ret = os.system(cmd)
    if ret != 0:
        print_console('Failed to build the Docker image')
        exit(-1)


def handle_build(args, config):
    """Handle build subcommand"""
    build_docker_image(args.dest)


def handle_doc(args, config):
    print_console("Generating documentation")
    ret = os.system('pdoc --html --config show_source_code=False -o docs --force app ')
    if ret != 0:
        exit(-1)
    print_console("\nDocumentation generated at docs/app/index.html\n"
                  + f"   Open in browser: file:///{WORKING_DIR}/docs/app/index.html")


def delayed_print(msgs: list, delay=3.0):
    def print_msgs():
        for m in msgs:
            print_console(m)

    from threading import Timer
    r = Timer(delay, print_msgs)
    r.start()

    return r


def handle_run(args, config):
    """Handle run subcommand"""
    dest = args.dest

    if dest == 'prod':
        print_console("Running the project in production preview mode")
    elif dest == 'dev':
        print_console("Running the project in development mode")

    # docker image build
    build_docker_image(dest)

    msgs = []
    # docker-compose up
    if dest == 'dev':
        msgs.append("Your app will be running at http://localhost:8888\n"
                    + "\t You can also access JuptyerLab at http://localhost:8889/lab")
    elif dest == 'prod':
        msgs.append("Your app will be running at http://localhost:8888/")

    print_console("Starting the Docker container (this may take a while) ...")
    if not args.verbose:
        print(f"\t Docker compose logs are being written to file:///{WORKING_DIR}/container/{dest}/docker-compose.log\n"
              + "\t You can use -v or --verbose option to see the logs.")

    msgs.append("Press Ctrl+C to stop the container")
    timer = delayed_print(msgs)

    cmd = f'cd container/{dest} && docker-compose up --remove-orphans'
    if not args.verbose:
        cmd += ' &> docker-compose.log'
    ret = os.system(cmd)
    if ret != 0 and ret != 33280 and not args.verbose:
        print_console(
            f'Failed to start the Docker container. Please check the logs in file:///{WORKING_DIR}/container/{dest}/docker-compose.log')
        exit(-1)

    print_console("Docker container stopped")
    timer.cancel()


def handle_deploy(args, config):
    """Handle deploy subcommand"""
    if args.target == 'registry':
        if 'registry_url' not in config:
            registry_url = get_input("Enter the Docker registry URL", 'docker.io')
            # validate the registry URL
            if registry_url[:4] == 'http':
                registry_url = registry_url.split('//')[1]
            if registry_url[-1] == '/':
                registry_url = registry_url[:-1]

            if registry_url == 'docker.io':
                registry_namespace = get_input("Enter the docker.io username")
            else:
                registry_namespace = get_input("Enter the Docker registry namespace (optional)", optional=True)

            registry_image_name = get_input("Enter the remote image name", config['project_name'])

            config['registry_url'] = registry_url
            config['registry_namespace'] = registry_namespace
            config['registry_image_name'] = registry_image_name
            save_config(config)
        else:
            config = load_config()
            registry_url = config['registry_url']
            registry_namespace = config['registry_namespace']
            registry_image_name = config['registry_image_name']

        project_name = config['project_name']

        ret = subprocess.run(['docker', 'images', '-q', 'jpr'], stdout=subprocess.PIPE)
        if ret.stdout.decode('utf-8') == '':
            # print_console('No Docker image found. Please run "japper build prod" first.')
            print_console('No Docker image found. Building the Docker image...')
            build_docker_image('prod')

        print_console("Logging in to the Docker registry...")
        run_command(f'docker login {config["registry_url"]}', 'Failed to login to the Docker registry', print_cmd=True)

        print_console("Tagging the Docker image...")
        if registry_url == 'docker.io':
            full_image_name = f'{registry_namespace}/{registry_image_name}:{args.tag}'
        else:
            if registry_namespace:
                full_image_name = f'{registry_url}/{registry_namespace}/{registry_image_name}:{args.tag}'
            else:
                full_image_name = f'{registry_url}/{registry_image_name}:{args.tag}'
        run_command(f'docker tag {project_name} {full_image_name}', 'Failed to tag the Docker image', print_cmd=True)

        print_console("Uploading the Docker image to the registry...")
        run_command(f'docker push {full_image_name}', 'Failed to upload the Docker image', print_cmd=True)

        print_console(f"Successfully uploaded the Docker image to {full_image_name}")


def handle_add(args, config):
    """Handle add subcommand"""
    if args.component == 'page':
        page_name = get_input("Enter the new page name", allow_spaces=True)
        icon = get_input(
            "Enter the material design icon name (optional) (e.g. mdi-home or home)\n" +
            " (You can check the full list of icons here: https://pictogrammers.github.io/@mdi/font/7.4.47)",
            optional=True)
        if icon and icon[:4] != 'mdi-':
            icon = 'mdi-' + icon

        snake_name = snake(page_name)
        if snake_name == page_name:
            page_msg = f"Page {page_name}"
        else:
            page_msg = f"Page {page_name} ({snake_name})"
        if os.path.exists(f'app/presenters/{snake_name}') or os.path.exists(
                f'app/views/{snake_name}') or os.path.exists(f'app/models/{snake_name}'):
            print_console(page_msg + " already exists")
            exit(-1)
        add_page(page_name, icon=icon, verbose=True)


def main():
    """
    japper command line interface main parser
    """
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(dest='subcommand', required=True)
    subparsers.add_parser('init', help="Initiate a new Japper project")
    parser = subparsers.add_parser('build', help="Build this Japper project")
    parser.add_argument('dest', choices=['dev', 'prod'], help="destination")

    parser = subparsers.add_parser('add', help="Add a new component to this Japper project")
    parser.add_argument('component', choices=['page'], help="component")

    parser = subparsers.add_parser('run', help="Run this Japper project using Docker")
    parser.add_argument('dest', choices=['dev', 'prod'], help="destination")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode", default=False)

    parser = subparsers.add_parser('deploy', help="Deploy this Japper project")
    parser.add_argument('target', choices=['registry'], help="target")
    parser.add_argument('-t', '--tag', help="tag", default='latest')

    parser = subparsers.add_parser('doc', help="Generate documentation")

    args = main_parser.parse_args()

    if args.subcommand == 'init':
        project_name, project_title = init_project()
        # save inputs to japper config file
        save_config({'project_name': project_name, 'project_title': project_title})
    else:  # other than init
        config = load_config()
        if 'project_name' not in config:
            print("No project found. Please run 'japper init' first.")
            exit(-1)
        if args.subcommand == 'build':
            handle_build(args, config)
        elif args.subcommand == 'add':
            handle_add(args, config)
        elif args.subcommand == 'run':
            handle_run(args, config)
        elif args.subcommand == 'deploy':
            handle_deploy(args, config)
        elif args.subcommand == 'doc':
            handle_doc(args, config)


if __name__ == '__main__':
    main()
