# to compress new Comm package issue on Sphinx https://github.com/jupyter-widgets/ipywidgets/pull/3533
import ipykernel.ipkernel  # noqa

from IPython.display import HTML
from IPython.display import display
import ipywidgets as ipyw

from .app_main_view import AppMainView
from . import utils
from .debug import is_dev, debug_view
from .widgets import NavigationMenu
from .page import Page


def init_js_output():  # deprecated
    """
    Initialize the output widget for JS. We need this approach to avoid blank space at the bottom of the page when
    new JS is executed.
    """
    output = ipyw.Output(layout={'display': 'none'})
    display(output)
    utils.set_js_output(output)


def inject_files():
    utils.inject_html('global.html')


class JapperAppMain:

    def __init__(self):
        self.app_name = None
        self.nav_menu = None
        self.main_view = None
        self.pages = []
        self.default_page = None

    def init_app(self, app_name: str = 'Japper App', favicon_path: str = None):
        """
        Initialize the app

        :param app_name: Name of the app
        :param favicon_path: Path to the favicon
        """
        # init_js_output()  # deprecated
        self.main_view = AppMainView()
        self.app_name = app_name
        utils.set_page_title(app_name)
        if favicon_path:
            utils.set_favicon(favicon_path)

        self.add_custom_html('app/assets/custom.html')

        # if dev mode, show the debug view
        if is_dev():
            debug_view.display_debug_view()

    def set_navigation_menu(self, mode: str = 'top', logo: str = None, title: str = None, nav_width: str = '230px'):
        """
        Set the navigation menu

        :param mode: 'top' or 'side'
        :param logo: Path to the logo
        :param title: Title of the navigation menu
        :param nav_width: Width of the navigation menu. Only applicable for 'side' mode
        """

        if title is None:
            title = self.app_name

        self.nav_menu = NavigationMenu(mode=mode,
                                       title=title,
                                       logo=logo,
                                       nav_width=nav_width)

    def add_page(self, page: Page, default=False):
        """
        Add a page to the app and navigation menu if available

        :param page: Page object
        :param default: Set this page as the default page
        """
        self.pages.append(page)
        if default:
            self.default_page = page

        if self.nav_menu:
            self.nav_menu.add_menu(page)

    def start_app(self):
        """
        Start the app
        """

        inject_files()
        if self.nav_menu:
            self.__init_navigation_menu()

        self.__preload_contents()

        self.main_view.render()

        self.__connect_util_funcs()
        display(self.main_view)
        self.show_page(page=self.default_page)

    def show_page(self, index: int = None, name: str = None, page: Page = None):
        """
        Show a page by index, name, or page object
        """
        if index is not None:
            self.main_view.set_content(self.pages[index].get_content())
        elif name is not None:
            for i, page in enumerate(self.pages):
                if page.name == name:
                    self.main_view.set_content(page.get_content())
                    index = i
                    break
        elif page is not None:
            self.main_view.set_content(page.get_content())
            index = self.pages.index(page)

        if self.nav_menu:
            self.nav_menu.update_nav_buttons_active_by_index(index)

    def __init_navigation_menu(self):
        self.nav_menu.render()
        self.main_view.set_nav_menu(self.nav_menu)
        self.nav_menu.connect_to_main_view(self.main_view)
        utils.set_nav_menu(self.nav_menu)

    def __preload_contents(self):
        for page in self.pages:
            page.render()

    def add_custom_html(self, filepath):
        display(HTML(filename=filepath))

    def __connect_util_funcs(self):
        """
        Connect utility functions from the main controller
        """
        utils.set_external_funcs(
            self.main_view.loading_dialog.show_loading,
            self.main_view.loading_dialog.hide_loading,
            self.main_view.toast_alert.alert,
            self.show_page
        )
