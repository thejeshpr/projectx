import importlib
import os


# mod = importlib.import_module('crdko')

# print(mod.scrape())


def get_scrapper(name):

    parent_path = os.path.dirname(os.path.realpath(__file__))
    base_path = os.path.dirname(parent_path)
    #base_path = "/home/ubuntu/pyenvs/projectx_dev/src/projectx/crawler_backend"
    files = os.listdir(parent_path)
    # files = os.listdir("./crawler_backend")
    # print(parent_path, base_path)

    module_files = list(filter(lambda x: x.endswith(".py") and x.startswith("cb_"), files))

    scrpr_mod_name = f"{name}.py"

    if scrpr_mod_name in module_files:
        mod = importlib.import_module(name)
        if hasattr(mod, "scrape"):
            return mod.scrape
    else:
        raise Exception(f"invalid scrapper name: {name}")
        # print ("No Module found")

