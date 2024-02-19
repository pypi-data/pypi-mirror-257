class BasePresenter:
    def __init__(self) -> None:
        self.view = None
        self.model = None

    def render(self, **kwargs):
        self.view.render()
        return self.view
