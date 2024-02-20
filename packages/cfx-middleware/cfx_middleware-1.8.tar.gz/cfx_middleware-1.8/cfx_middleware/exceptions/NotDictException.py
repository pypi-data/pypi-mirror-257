class NotDictException(Exception):
    pass


def is_dict(variable):
    if not isinstance(variable, dict):
        raise NotDictException(
            "The data provided is not a dict, please review the data"
        )
