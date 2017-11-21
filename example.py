import importlib
import pkgutil

# import logging
# logging.basicConfig(level=logging.DEBUG)

import samples.tools

def run_all_samples():
    for _, sample_name, _ in pkgutil.walk_packages(samples.__path__):
        if not sample_name.endswith("samples"):
            continue
        print("Executing sample from ", sample_name)
        sample_module = importlib.import_module('samples.'+sample_name)
        samples.tools.execute_samples(sample_module.__dict__)

if __name__ == "__main__":
    run_all_samples()
