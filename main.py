#!/usr/bin/env python3
# coding: utf-8


import inspect
import os
import sys
import traceback

from jobs.base import JobBase

WEB_HOOK_ID_ENV_NAME = "FEISHU_WEB_HOOK_ID"


def usage():
    """
    Show usage
    """
    print("Usage: python main.py <module> [args ...]")


def load_all_modules(dir_name: str = "jobs") -> list[str]:
    """
    Load all modules in
    """
    current_file = os.path.abspath(__file__)
    current_path = os.path.dirname(current_file)
    module_path = "{0}/{1}".format(current_path, dir_name)

    for filename in os.listdir(module_path):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name_base = filename[:-3]
        module_name = "{0}.{1}".format(dir_name, module_name_base).replace("/", ".")
        module = __import__(module_name, globals(), locals())
        for name, obj in inspect.getmembers(sys.modules[module_name]):
            if not inspect.isclass(obj):
                continue

            if issubclass(obj, JobBase) and obj is not JobBase:
                yield filename, name, obj


def load_web_hook_id() -> str:
    """
    Load FEISHU web hook ID from environment variable.
    """
    id = os.environ.get(WEB_HOOK_ID_ENV_NAME)
    return id or ""


def is_dry_run() -> bool:
    """
    load DRY_RUN from environment variable.
    """
    value = os.environ.get("DRY_RUN", "")
    return len(value) > 0

def main():
    """
    Main entry
    """
    web_hook_id = load_web_hook_id()
    if not web_hook_id:
        print("FEISHU web hook ID is not set")
        return
    
    dry_run = is_dry_run()
    args = sys.argv[1:]
    for filename, name, module in load_all_modules():
        try:
            print("load module {0} from {1}: {2}".format(name, filename, module))
            m = module(web_hook_id)
            m.dry_run = dry_run
            m.run(args)

        except Exception as ex:
            print("Error: {0}".format(ex))
            print("%s" % traceback.format_exc())


if __name__ == "__main__":
    main()
