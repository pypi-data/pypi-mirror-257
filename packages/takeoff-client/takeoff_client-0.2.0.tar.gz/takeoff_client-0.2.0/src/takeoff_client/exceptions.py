class TakeoffError(Exception):
    def __init__(self, status_code, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code
