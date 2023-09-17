def init(logging):
    global log
    log = bool(logging)


def write(message):
    if log:
        print(message)