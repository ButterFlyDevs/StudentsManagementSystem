import werkzeug.exceptions as exceptions
import flask
import functools
import inspect
import logging
import six

logger = logging.getLogger(__name__)

# https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md#data-types
TYPE_MAP = {'integer': int,
            'number': float,
            'string': str,
            'boolean': bool,
            'array': list,
            'object': dict}  # map of swagger types to python types


def get_function_arguments(function):  # pragma: no cover
    """
    Returns the list of arguments of a function

    :type function: Callable
    :rtype: list[str]
    """
    if six.PY3:
        return list(inspect.signature(function).parameters)
    else:
        return inspect.getargspec(function).args


def make_type(value, type):
    type_func = TYPE_MAP[type]  # convert value to right type
    return type_func(value)


def get_val_from_param(value, query_param):
    if query_param["type"] == "array":  # then logic is more complex
        if query_param.get("collectionFormat") and query_param.get("collectionFormat") == "pipes":
            parts = value.split("|")
        else:  # default: csv
            parts = value.split(",")
        return [make_type(part, query_param["items"]["type"]) for part in parts]
    else:
        return make_type(value, query_param["type"])


def parameter_to_arg(parameters, function):
    """
    Pass query and body parameters as keyword arguments to handler function.

    See (https://github.com/zalando/connexion/issues/59)
    :type body_schema: dict|None
    :type parameters: dict|None
    """
    body_parameters = [parameter for parameter in parameters if parameter['in'] == 'body'] or [{}]
    body_name = body_parameters[0].get('name')
    query_types = {parameter['name']: parameter
                   for parameter in parameters if parameter['in'] == 'query'}  # type: dict[str, str]
    arguments = get_function_arguments(function)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger.debug('Function Arguments: %s', arguments)

        try:
            request_body = flask.request.json
        except exceptions.BadRequest:
            request_body = None

        # Add body parameters
        if request_body is not None:
            if body_name not in arguments:
                logger.debug("Body parameter '%s' not in function arguments", body_name)
            else:
                logger.debug("Body parameter '%s' in function arguments", body_name)
                kwargs[body_name] = request_body

        # Add query parameters
        for key, value in flask.request.args.items():
            if key not in arguments:
                logger.debug("Query Parameter '%s' not in function arguments", key)
            else:
                logger.debug("Query Parameter '%s' in function arguments", key)
                query_param = query_types[key]
                logger.debug('%s is a %s', key, query_param)
                kwargs[key] = get_val_from_param(value, query_param)

        return function(*args, **kwargs)

    return wrapper
