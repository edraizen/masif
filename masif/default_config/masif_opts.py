import os
import json
import tempfile
import importlib
import collections.abc

masif_opts = {}

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def make_paths(d, this_dir=None):
    for k, v in d.items():
        if isinstance(v, collections.abc.Mapping):
            make_paths(v)
        elif k.endswith("_dir"):
            if v.startswith("{masif_source}"):
                v = v.format(masif_source=os.dirname(os.dirname(__file__)))
            if v == "{tmp_dir}":
                #Set tempdir
                v = v.format(tmp_dir=tempfile.gettempdir())
            if this_dir is not None and v.startswith("{this_dir}"):
                v = v.format(masif_source=os.dirname(os.dirname(__file__)))
            if not os.path.isdir(v):
                os.make_dirs(v, exist_ok=True)

def read_config_file(f):
    with open(default_config_path) as fh:
        config = json.load(fh)
    return config

def update_config(old, new=None):
    global masif_opts

    if isinstance(old, collections.abc.Mapping):
        pass
    elif isinstance(old, str) and old in masif_opts:
        old = masif_opts[old]
    elif isinstance(old, str) and os.path.isfile(old):
        old = read_config_file(f)
    else:
        raise KeyError("Invalid key or file")

    if isinstance(new, collections.abc.Mapping):
        pass
    elif isinstance(new, str) and os.path.isfile(old):
        new = read_config_file(f)
    else:
        if "masif" in new and "." in new:
            try:
                newobj = importlib.import_module(new, package=None)
                new_config_dir = os.path.dirname(newobj.__file__)
                new_config_file = os.path.join(new_config_dir, "custom_params.json")
                if os.path.isfile(new_config_file):
                    new = read_config_file(new_config_file)
                    new = make_paths(new_config_dir)
                else:
                    new = {}
                del newobj
            except ImportError:
                new = {}
        else:
            new = {}

    masif_opts = update(old, new)
    masif_opts = make_paths(masif_opts)

    return masif_opts

#Read in defaut config options
default_config_path = os.path.join(os.path.dirname(__file__), "masif_opts.json")

#Read in local config options in current directory if any
local_config_file = os.path.join(os.getcwd(), "masif_opts.json")

#Update default config options with local
masif_opts = update_config(default_config_path, local_config_file)