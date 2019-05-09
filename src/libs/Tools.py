class CustomPermissionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoSubcommand(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoRolesGiven(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoReactMethod(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BooruNoPosts(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RolesTooHigh(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoValidSelfRoles(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
