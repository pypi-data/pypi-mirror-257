import ipyvuetify as v
from functools import partial
from ..config import Config
from ..page import Page


class NavigationMenu:
    """
        Menu implementation using Vuetify's NavigationDrawer for the left side menu, and Toolbar for the top menu.
    """

    def __init__(self, title: str = None, nav_width: str = '230px',
                 mode: str = 'top', logo=None, icon_color: str = 'rgb(42, 53, 71)'):
        """
        :param title: Title of the navigation menu
        :param nav_width: Width of the navigation menu
        :param mode: 'top' or 'side'
        :param logo: Logo of the navigation menu
        :param icon_color: Icon color

        """
        self.title = title
        self.mode = mode
        self.logo = logo
        self.nav_width = nav_width
        self.icon_color = icon_color

        self.view = None
        self.main_view = None
        self.pages = []
        self.nav_buttons = []

    def add_menu(self, page: Page):
        """
        Add a menu item to the navigation menu

        :param page: Page object
        """
        self.pages.append(page)

    def render(self):
        if self.mode == 'top':
            self.view = self.create_navigation_bar()
        else:
            self.view = self.create_navigation_drawer()

        # click handler
        for i, button in enumerate(self.nav_buttons):
            button.on_event('click', partial(self.on_nav_clicked, button, self.pages[i]))

    def on_nav_clicked(self, clicked_item, page, *_):
        if self.main_view is not None:
            self.main_view.set_content(page.get_content())

        self.update_nav_buttons_active(clicked_item)

    def update_nav_buttons_active(self, clicked_item):
        for button in self.nav_buttons:
            button.class_list.remove('v-nav-active')
        clicked_item.class_list.add('v-nav-active')

    def update_nav_buttons_active_by_index(self, index):
        self.update_nav_buttons_active(self.nav_buttons[index])

    def create_navigation_drawer(self):
        nav_menu = v.NavigationDrawer(fixed=True,
                                      mini_variant=False,
                                      permanent=True,
                                      width=self.nav_width,
                                      )

        if self.title is not None:
            nav_menu.children = [
                v.List(class_='my-3', children=[
                    v.ListItem(children=[
                        v.Img(src=self.logo, width=Config.NavigationMenu.logo_size,
                              height=Config.NavigationMenu.logo_size, class_='mr-2') if self.logo else '',
                        v.ListItemTitle(class_='logo-text', style_=Config.NavigationMenu.title_text_style, children=[
                            self.title
                        ])
                    ]),

                ]),
                # v.Divider()
            ]

        buttons = []
        for page in self.pages:
            icon = page.icon if page.icon else ''
            buttons.append(v.ListItem(class_='py-1', link=True, children=[
                v.ListItemIcon(class_='mx-2', children=[
                    v.Icon(children=[icon], color=self.icon_color, size='16px')
                ]),
                v.ListItemContent(children=[
                    v.ListItemTitle(style_="color:#2A3547", children=[
                        page.name.upper()
                    ])
                ])
            ]))

        nav_menu.children = nav_menu.children + [v.List(dense=True, nav=True, children=buttons)]
        self.nav_buttons = buttons
        return nav_menu

    def create_navigation_bar(self):
        nav_bar = v.Toolbar(app=True,
                            style_=f"""
                            position:fixed;
                            width:100%;
                            height:64px;
                            z-index: 10;
                            padding: 0 calc((100% - {Config.Content.width['top_nav_mode']}) / 2);"""
                            )

        buttons = []
        for page in self.pages:
            button = v.Btn(
                height='50px !important',
                flat=True,
                text=True,
                style_="color:#2A3547;border-radius:20px !important;",
            )
            if page.icon:
                button.children = [v.Icon(children=[page.icon], color=self.icon_color, size='16px')]

            button.children = button.children + [page.name.upper()]
            buttons.append(button)

        nav_bar.children = [
            v.ToolbarTitle(class_='d-flex', children=[
                v.Img(src=self.logo, class_='mr-2', width=Config.NavigationMenu.logo_size,
                      height=Config.NavigationMenu.logo_size) if self.logo else '',
                v.Html(tag='span', class_='logo-text', style_=Config.NavigationMenu.title_text_style,
                       children=[self.title if self.title else ''])
            ]),
            v.Spacer(),
            v.ToolbarItems(children=buttons, class_='align-center')
        ]

        self.nav_buttons = buttons
        return nav_bar

    def connect_to_main_view(self, main_view):
        self.main_view = main_view

    def move_to(self, menu_index):
        self.on_nav_clicked(self.nav_buttons[menu_index])
