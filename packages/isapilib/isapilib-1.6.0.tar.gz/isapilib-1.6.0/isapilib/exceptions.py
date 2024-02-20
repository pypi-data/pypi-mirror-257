class SepaException(BaseException):

    def __init__(self, description, user=None, branch=None):
        self.user = user
        self.branch = branch
        super().__init__(description)


class AfectarException(BaseException):

    def __init__(self, ok, ok_ref):
        self.ok = ok
        self.ok_ref = ok_ref
        super().__init__(f'{self.ok}: {self.ok_ref}')
