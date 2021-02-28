"""Sort the given list in the way that humans expect."""

# thanks https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
# but modifying in-place seems rude
# http://www.compciv.org/guides/python/fundamentals/lists-mutability/
import re


def sort_nicely(things: list) -> list:
    """Sort the given list in the way that humans expect."""

    new_list = things.copy()
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    new_list.sort(key=alphanum_key)
    return new_list
