class Non200HttpStatusError(RuntimeError):
    def __init__(self, status_code: int, description: str = None):
        if status_code == 200:
            raise ValueError('Cannot init Non200HttpStatusError with status_code=200')

        msg = f'Response returned HTTP{status_code}'
        if description is not None:
            msg += f': {description}'

        super().__init__(msg)