from utility.debug import debug


def function_called_coroutine(function):
    async def debug_message(*args, **kwargs):
        debug(f'Pass on {function.__name__}')
        return await function(*args, **kwargs)

    return debug_message


def function_called(function):
    def debug_message(*args, **kwargs):
        debug(f'Pass on {function.__name__}')
        return function(*args, **kwargs)

    return debug_message
