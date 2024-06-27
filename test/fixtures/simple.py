import base64

def get_foo():
    return "foo"

def main():
    base64.b64encode("asd")
    get_foo()

def something():
    return {
        "asd": get_foo(),
    }
