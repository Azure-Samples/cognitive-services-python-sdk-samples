"""Sample launcher.

This file is just the samples launcher. Nothing here os related
to Cognitive Services. Look into the "samples" folder for actual code
"""

import importlib
import pkgutil

# import logging
# logging.basicConfig(level=logging.DEBUG)

import samples.tools


def run_all_samples():
    for _, section_name_name, ispkg in pkgutil.walk_packages(samples.__path__):
        if not ispkg:
            continue
        section_package_name = "samples."+section_name_name
        section_package = importlib.import_module(section_package_name)
        for _, sample_name, _ in pkgutil.iter_modules(section_package.__path__):
            sample_module = importlib.import_module(
                section_package_name+"."+sample_name)
            subkey_env_name = getattr(
                sample_module, "SUBSCRIPTION_KEY_ENV_NAME", None)
            if not subkey_env_name:
                continue
            print("Executing sample from ", sample_name)
            try:
                samples.tools.execute_samples(
                    sample_module.__dict__, subkey_env_name)
            except samples.tools.SubscriptionKeyError as err:
                print("{}\n".format(err))


if __name__ == "__main__":
    run_all_samples()
