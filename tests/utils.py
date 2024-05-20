from dataclasses import fields


def check_unknown_things(n, c, p):
    if type(c) is list:
        c = c[0]
    if '__dataclass_fields__' in dir(c):
        for _field in fields(c):
            next_p = p.copy()
            next_p.append(_field.name)
            check_unknown_things(_field.name, getattr(c, _field.name), next_p)
    else:
        if n == 'unknown_things' and c:
            raise Exception('New params in API! ' + ' -> '.join(p), c)


def check_api_update(_dataclass):
    """ Only for dataclasses | Find new params in API

    :return:
    """
    for field in fields(_dataclass):
        path = [field.name]
        check_unknown_things(field.name, getattr(_dataclass, field.name), path)
