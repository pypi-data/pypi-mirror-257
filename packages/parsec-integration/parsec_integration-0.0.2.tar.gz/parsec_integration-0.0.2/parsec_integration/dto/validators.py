

def guid_validate(value):
    res = value.split("-")
    if len(res) != 5:
        raise ValueError("Incorrect Guid")
    code = 8, 4, 4, 4, 12
    ind = 0
    for c in res:
        if len(c) != code[ind]:
            raise ValueError("Incorrect Guid")
        ind += 1
    return value


def long_validate(value):
    return int(value, 2)
