import os
import shutil

from .globals import InitConfig, create_file, get_input, get_yn_input, STDOUT_COLOR, render_template, \
    add_page


def init_project():
    print("Initiating a new Japper project")

    # get project information
    project_name = get_input("Enter project name using snake case (e.g. japper_project)", color=STDOUT_COLOR.HEADER)
    camel_project_name = project_name.replace('_', ' ').replace('-', ' ')
    camel_project_name = ' '.join([word.capitalize() for word in camel_project_name.split(' ')])
    project_title = get_input(f"Enter project title", default=camel_project_name,
                              allow_spaces=True)

    # get customizations
    # ret = get_yn_input("Do you want to customize the default app templates?")
    # if ret:

    # Create a new directory for the project
    for dir_str in InitConfig.DIRS_TO_CREATE:
        print(f'Creating directory: {dir_str}')
        os.makedirs(dir_str, exist_ok=True)

    # copy files from static folder
    static_path = os.path.dirname(__file__) + '/static/'
    for root, dirs, files in os.walk(static_path):
        for file in files:
            if file == '.DS_Store':
                continue
            src_path = os.path.join(root, file)
            dst_path = os.path.join(root.replace(static_path, ''), file)
            if file == 'gitignore':
                dst_path = os.path.join(root.replace(static_path, ''), '.gitignore')

            print(f'Creating file: {dst_path}')
            shutil.copy(src_path, dst_path)

    # create app_main.py
    create_file('app/__init__.py', "from .app_main import AppMain\n")
    render_template('app.app_main.py.jinja2', navigation_mode='top')

    # create config.py
    render_template('app.commons.config.py.jinja2', project_title=project_title)

    # create home page
    render_template('app.presenters.home.py.jinja2')
    render_template('app.views.home.py.jinja2')
    render_template('app.models.home.py.jinja2')

    # create __init__.py files
    create_file('app/presenters/__init__.py', "from .home import HomePresenter\n")
    create_file('app/views/__init__.py', "from .home import HomeView\n")
    create_file('app/models/__init__.py', "from .home import HomeModel\n")
    render_template('app.commons.__init__.py.jinja2')

    # add tool page
    add_page('Tool', 'mdi-cog')

    # create docker-compose files
    render_template('container.dev.docker-compose.yml.jinja2', project_name=project_name)
    render_template('container.prod.docker-compose.yml.jinja2', project_name=project_name)

    # create Readme
    render_template('README.md.jinja2', project_title=project_title)

    print("Project initiated successfully")

    return project_name, project_title
