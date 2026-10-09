"""Minimal, dependency-free JSON Schema draft-07 validator.

Why this exists: a design-repo is handed over as a standalone folder (or a zip),
and the self-containment test copies it to an isolated directory and re-runs
every script there. Depending on `jsonschema` being pip-installed would make
that test pass or fail based on the host environment rather than on the repo's
own contents. So the repo ships its own validator and has ZERO external
dependencies -- stdlib only.

Supported keywords, which is exactly the set pagespec.schema.json uses:
  type, enum, const, properties, required, additionalProperties,
  items, minItems, maxItems, minimum, maximum, pattern, minLength, maxLength,
  allOf, anyOf, oneOf, not, if/then/else.
Unknown keywords (including the x-* annotations and the maxWords budgets the
semantic validator reads) are ignored, per the spec.

This was cross-checked against the reference `jsonschema` package (4.25.1) on
the real schema, the bundled example and every adversarial mutation in
schema/tests/adversarial_test.py; both agree on every case. See
extraction/verify_all.py --cross-check.
"""
import re


class SchemaError(Exception):
    pass


_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _is_type(value, name):
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name in _TYPES:
        return isinstance(value, _TYPES[name]) and not (
            name != "boolean" and isinstance(value, bool)
        )
    raise SchemaError("unsupported type: %r" % name)


def _fmt(path):
    return "$" + "".join(
        "[%d]" % p if isinstance(p, int) else ".%s" % p for p in path
    )


def iter_errors(instance, schema, path=()):
    """Yield (pathstring, message) for every validation failure."""
    if schema is True or schema == {}:
        return
    if schema is False:
        yield _fmt(path), "schema is false: nothing is valid here"
        return
    if not isinstance(schema, dict):
        raise SchemaError("schema must be an object or boolean")

    if "type" in schema:
        want = schema["type"]
        names = want if isinstance(want, list) else [want]
        if not any(_is_type(instance, n) for n in names):
            yield _fmt(path), "expected type %s, got %s" % (
                "/".join(names),
                type(instance).__name__,
            )
            return

    if "const" in schema and instance != schema["const"]:
        yield _fmt(path), "must be the constant %r, got %r" % (
            schema["const"],
            instance,
        )
    if "enum" in schema and instance not in schema["enum"]:
        yield _fmt(path), "%r is not one of %r" % (instance, schema["enum"])

    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            yield _fmt(path), "%r does not match pattern %r" % (
                instance,
                schema["pattern"],
            )
        if "minLength" in schema and len(instance) < schema["minLength"]:
            yield _fmt(path), "shorter than minLength %d" % schema["minLength"]
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            yield _fmt(path), "longer than maxLength %d" % schema["maxLength"]

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            yield _fmt(path), "%r is below minimum %r" % (instance, schema["minimum"])
        if "maximum" in schema and instance > schema["maximum"]:
            yield _fmt(path), "%r is above maximum %r" % (instance, schema["maximum"])

    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                yield _fmt(path), "missing required property %r" % key
        for key, value in instance.items():
            if key in props:
                for err in iter_errors(value, props[key], path + (key,)):
                    yield err
        extra = schema.get("additionalProperties", True)
        if extra is not True:
            unknown = [k for k in instance if k not in props]
            if extra is False:
                for k in sorted(unknown):
                    yield _fmt(path + (k,)), "additional property %r is not allowed" % k
            else:
                for k in sorted(unknown):
                    for err in iter_errors(instance[k], extra, path + (k,)):
                        yield err

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            yield _fmt(path), "has %d items, minItems is %d" % (
                len(instance),
                schema["minItems"],
            )
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            yield _fmt(path), "has %d items, maxItems is %d" % (
                len(instance),
                schema["maxItems"],
            )
        items = schema.get("items")
        if isinstance(items, dict):
            for i, value in enumerate(instance):
                for err in iter_errors(value, items, path + (i,)):
                    yield err
        elif isinstance(items, list):
            for i, sub in enumerate(items):
                if i < len(instance):
                    for err in iter_errors(instance[i], sub, path + (i,)):
                        yield err

    for sub in schema.get("allOf", []):
        for err in iter_errors(instance, sub, path):
            yield err

    if "anyOf" in schema:
        if not any(
            not list(iter_errors(instance, sub, path)) for sub in schema["anyOf"]
        ):
            yield _fmt(path), "does not match any of the %d anyOf branches" % len(
                schema["anyOf"]
            )

    if "oneOf" in schema:
        hits = sum(
            1 for sub in schema["oneOf"] if not list(iter_errors(instance, sub, path))
        )
        if hits == 0:
            yield _fmt(path), "does not match any of the %d oneOf branches" % len(
                schema["oneOf"]
            )
        elif hits > 1:
            yield _fmt(path), "matches %d oneOf branches, expected exactly 1" % hits

    if "not" in schema and not list(iter_errors(instance, schema["not"], path)):
        yield _fmt(path), "must not match the 'not' schema"

    if "if" in schema:
        matched = not list(iter_errors(instance, schema["if"], path))
        branch = schema.get("then") if matched else schema.get("else")
        if branch is not None:
            for err in iter_errors(instance, branch, path):
                yield err


def validate(instance, schema):
    return sorted(iter_errors(instance, schema), key=lambda e: e[0])


def check_schema(schema):
    """Shallow sanity check that the schema only uses supported keywords."""
    supported = {
        "$schema", "$id", "title", "description", "type", "enum", "const",
        "properties", "required", "additionalProperties", "items", "minItems",
        "maxItems", "minimum", "maximum", "pattern", "minLength", "maxLength",
        "allOf", "anyOf", "oneOf", "not", "if", "then", "else", "default",
    }
    unsupported = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("properties",):
                    for sub in value.values():
                        walk(sub)
                    continue
                if key.startswith("x-") or key in (
                    "note", "notes", "maxWords", "measuredLongestRealInstance",
                    "measuredValue", "settable", "hardConstraint", "forbiddenFields",
                    "forbiddenFieldsReason", "assetRoleEnumRef", "allowedRoles",
                    "mantine", "evidence", "rgb", "usage", "measuredFrom",
                ):
                    continue
                if key not in supported and not isinstance(value, (dict, list)):
                    unsupported.add(key)
                walk(value)
        elif isinstance(node, list):
            for sub in node:
                walk(sub)

    walk(schema)
    return sorted(unsupported)
