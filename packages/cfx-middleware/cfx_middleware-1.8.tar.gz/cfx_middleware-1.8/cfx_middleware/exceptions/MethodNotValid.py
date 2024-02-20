from cfx_middleware.enums.MethodsEnum import Methods


class MethodNotValid(Exception):
    pass


def validate_method(method):
    if method not in Methods.__members__:
        methods_valids = ", ".join(member.value for member in Methods)

        raise MethodNotValid(
            f"The method provided '{method}' doesn't exist, methods available are: {methods_valids}"
        )
