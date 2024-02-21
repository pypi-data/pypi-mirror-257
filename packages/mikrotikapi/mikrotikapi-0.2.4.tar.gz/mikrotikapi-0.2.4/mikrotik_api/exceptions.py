class NotCreated(Exception):
    def __init__(self):
        Exception.__init__(self, "Object not created")


class DoesNotExist(Exception):
    def __init__(self, **kwargs):
        Exception.__init__(self, f"Does Not Exist {kwargs=}")


class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
