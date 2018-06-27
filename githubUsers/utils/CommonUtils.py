import inspect

def whoami():
    return inspect.getouterframes(inspect.currentframe())[1].function
