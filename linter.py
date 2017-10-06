#!/usr/bin/env python
import json
import glob
from collections import OrderedDict
import re
import sys
import inspect
import importlib
import argparse


def warn(msg, *args, **kwargs):
    print("[WARN]", msg.format(*args, **kwargs))


def normalized_type(schema):
    type_ = schema.get("type", [])
    if isinstance(type_, list):
        return type_
    return [type_]


def guess_indentation(f):
    f.readline()
    second_line = f.readline()
    f.seek(0)
    match = re.match(" +", second_line)
    if match:
        return len(match.group(0))
    return 2


def walk_subschemas(schema, path=[]):
    yield schema, path
    if "properties" in schema:
        for k, v in schema["properties"].items():
            yield from walk_subschemas(v, path + [k])
    if "items" in schema:
        yield from walk_subschemas(schema["items"], path + ["items"])


def walk_missing_additional_properties(schema):
    for subschema, path in walk_subschemas(schema):
        is_missing = ("type" in subschema
                      and "object" in normalized_type(subschema)
                      and "additionalProperties" not in subschema)
        if is_missing:
            yield subschema, path


def all_schemas(args):
    files = glob.glob(args.module + "/schemas/*.json")
    for fname in files:
        with open(fname) as f:
            schema = json.loads(f.read(), object_pairs_hook=OrderedDict)
        yield fname, schema


def additional_properties_handling(args):
    for fname, schema in all_schemas(args):
        for subschema, path in walk_missing_additional_properties(schema):
            if args.autofix_additional_properties:
                subschema["additionalProperties"] = False
            else:
                warn('"additionalProperties" not found: {} {}', fname, path)
        if args.autofix_additional_properties:
            with open(fname) as f:
                identation = guess_indentation(f)
            with open(fname, "w") as f:
                f.write(json.dumps(schema, indent=identation))
                f.write("\n")


def empty_schemas_handling(args):
    for fname, schema in all_schemas(args):
        for subschema, path in walk_subschemas(schema):
            if subschema == {}:
                warn("empty schema found: {} {}", fname, path)


def check_for_critical_log(mod):
    source = inspect.getsource(mod.main)
    if "critical" not in source:
        warn("no critical log found in main function")


def main(args):
    mod = importlib.import_module(args.module)
    additional_properties_handling(args)
    empty_schemas_handling(args)
    check_for_critical_log(mod)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--autofix-additional-properties", action="store_true")
    args = parser.parse_args()
    main(args)
