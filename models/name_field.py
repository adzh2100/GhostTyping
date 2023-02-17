from models.input_field import InputField

class NameField(InputField):
    def __init__(self, x, y, text):
        InputField.__init__(self, x, y, 320, 32, text)
