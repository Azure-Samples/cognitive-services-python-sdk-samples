import importlib
try:
    from inspect import getfullargspec as get_arg_spec
except ImportError:
    from inspect import getargspec as get_arg_spec
import os
import pkgutil
import sys
import types

import samples

def run_example():
    try:
        subscription_key = os.environ["SUBSCRIPTION_KEY"]
    except KeyError:
        sys.exit("You must set the env variable SUBSCRIPTION_KEY to execute this sample")

    def start_sample(func):
        print("Sample:", func.__doc__,"\n")
        func(subscription_key)
        print("\n\n")

    for _, sample_name, _ in pkgutil.walk_packages(samples.__path__):
        sample_module = importlib.import_module('samples.'+sample_name)
        for func in list(sample_module.__dict__.values()):
            if not isinstance(func, types.FunctionType):
                continue
            args = get_arg_spec(func).args
            if 'subscription_key' in args:
                start_sample(func)

if __name__ == "__main__":
    run_example()
