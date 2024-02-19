from re import sub
import os
import yaml
from jinja2 import Environment, FileSystemLoader

# jinja2 environment
env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) + '/templates'))

CONFIG_FILENAME = 'japper.yml'


class STDOUT_COLOR:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InitConfig:
    DIRS_TO_CREATE = ['app', 'app/assets', 'app/commons', 'app/models', 'app/presenters', 'app/views', 'container',
                      'container/dev', 'container/prod']


def run_command(cmd, fail_msg=None, print_cmd=False):
    if print_cmd:
        print(f'Running command: {cmd}')
    ret = os.system(cmd)
    if ret != 0:
        if fail_msg:
            print_console(fail_msg)
        exit(-1)
    return ret


def print_console(msg):
    print(STDOUT_COLOR.HEADER + '[Japper] ' + STDOUT_COLOR.ENDC + msg)


def save_config(config):
    with open(CONFIG_FILENAME, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def load_config():
    if not os.path.exists(CONFIG_FILENAME):
        return {}
    with open(CONFIG_FILENAME, 'r') as f:
        return yaml.safe_load(f)


def get_input(prompt, default=None, optional=False, allow_spaces=False, color=None):
    if color:
        prompt = color + prompt + STDOUT_COLOR.ENDC
    while True:
        if default:
            user_input = input(f"{prompt}: [default: {default}] ")
            if not user_input:
                user_input = default
        else:
            user_input = input(prompt + ': ')
            if not user_input:
                if optional:
                    return None
                else:
                    print("This field is required")
                    continue

        if not allow_spaces and ' ' in user_input:
            print("This field cannot contain spaces")
            continue

        return user_input


def snake(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def camel(s):
    return ''.join([word.capitalize() for word in s.split(' ')])


def create_file(file_path, content=''):
    with open(file_path, 'w') as f:
        f.write(content)


def add_page(page_name: str, icon: str = None, verbose=False):
    snake_page_name = snake(page_name)
    camel_page_name = camel(page_name)

    file_presenter, file_view, file_model = (render_template('app.presenters.__base__.py.jinja2',
                                                             base_filename=snake_page_name,
                                                             page_name=camel_page_name),
                                             render_template('app.views.__base__.py.jinja2',
                                                             base_filename=snake_page_name,
                                                             page_name=camel_page_name),
                                             render_template('app.models.__base__.py.jinja2',
                                                             base_filename=snake_page_name,
                                                             page_name=camel_page_name))
    if verbose:
        print_console(f"Adding page files...\n{file_presenter}\n{file_view}\n{file_model}")

    # update __init__.py files
    with open('app/presenters/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}Presenter\n")
    with open('app/views/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}View\n")
    with open('app/models/__init__.py', 'a') as f:
        f.write(f"from .{snake_page_name} import {camel_page_name}Model\n")

    # update app_main.py
    with open('app/app_main.py', 'r') as f:
        lines = f.readlines()

    # add presenter
    for i in range(len(lines)):
        if 'from .presenters import' in lines[i]:
            lines[i] = lines[i].replace('from .presenters import',
                                        f'from .presenters import {camel_page_name}Presenter,')
            break

    # add page by backtracking from the end of the file
    addpage_code = f"self.add_page(Page(name='{page_name}', presenter={camel_page_name}Presenter()"
    if icon:
        addpage_code += f", icon='{icon}'"
    addpage_code += '))\n'

    for i in range(len(lines) - 1, -1, -1):
        if 'self.add_page(' in lines[i]:
            spaces = len(lines[i]) - len(lines[i].lstrip())
            lines.insert(i + 1, ' ' * spaces + addpage_code)
            break

    with open('app/app_main.py', 'w') as f:
        f.write(''.join(lines))
        f.write('\n')

    if verbose:
        print_console(
            f"Page {page_name} added successfully. " +
            "Please check you app_main.py file to make sure the page is added correctly." +
            " If not, please add it manually the following code:\n\n" + addpage_code)


def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_yn_input(prompt, default=None):
    while True:
        y_str = 'Y' if default else 'y'
        n_str = 'N' if default is False else 'n'

        print(prompt + f' [{y_str}/{n_str}]', end=' ')
        user_input = getch()
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        elif user_input == '\r' and default is not None:
            return default
        else:
            print("Invalid input. Please enter 'y' or 'n'")


def render_template(template_name, base_filename=None, **kwargs):
    template = env.get_template(template_name)
    content = template.render(**kwargs)
    tokens = template_name[:-7].split('.')  # remove .jinja2 and split by .
    if 'Dockerfile' in tokens[-1]:
        file_path = '/'.join(tokens)
    else:
        file_path = '/'.join(tokens[:-1]) + '.' + tokens[-1]
    if base_filename:
        file_path = file_path.replace('__base__', base_filename)

    create_file(file_path, content)

    return file_path
