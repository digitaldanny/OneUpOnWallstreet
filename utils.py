import inspect  # Need the stack for caller in 'needsImplementation'

def needsImplementation():
    print("-E- Needs implementation: {}".format(inspect.stack()[1][3]))

def print_info(message):
    print(message)

def print_warning(message):
    print("WARN: {}".format(message))

def print_error(message):
    print("ERROR: {}".format(message))