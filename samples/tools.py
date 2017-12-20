"""This file is just a sample launcher code.

Nothing is is related to Cognitive Services.
"""
try:
    from inspect import getfullargspec as get_arg_spec
except ImportError:
    from inspect import getargspec as get_arg_spec
import os
import sys
import types


class SubscriptionKeyError(Exception):
    pass


def start_sample(func, subscription_key):
    """Start the function and show its doc on output.
    """
    print("Sample:", func.__doc__,"\n")
    func(subscription_key)
    print("\n\n")


def execute_samples(module_globals, key_env_variable):
    """Execute samples based on a dict <name, function>
    """
    try:
        subscription_key = sys.argv[1] if len(sys.argv) >= 2 else os.environ[key_env_variable]
    except KeyError:
        raise SubscriptionKeyError("You need to either set the {} env variable.".format(key_env_variable))

    for func in list(module_globals.values()):
        if not isinstance(func, types.FunctionType):
            continue
        args = get_arg_spec(func).args
        if 'subscription_key' in args:
            start_sample(func, subscription_key)
