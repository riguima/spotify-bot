class InvalidLoginError(Exception):
    def __init__(self):
        super().__init__('Invalid Login')


class RegistrationError(Exception):
    def __init__(self):
        super().__init__('Registration Error')
