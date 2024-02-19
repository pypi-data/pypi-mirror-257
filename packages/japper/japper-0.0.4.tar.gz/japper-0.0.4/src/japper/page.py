from .base_presenter import BasePresenter


class Page:
    def __init__(self, name: str, presenter: BasePresenter, icon: str = None):
        self.name = name
        self.presenter = presenter
        self.icon = icon
        self.rendered = False

    def render(self):
        if not self.rendered:
            self.rendered = True
            self.presenter.render()

    def get_content(self):
        self.render()
        return self.presenter.view
