from dlmail.dlmail import DlMail
class config(DlMail):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def hello():
    return "Hello from dlmail!"
