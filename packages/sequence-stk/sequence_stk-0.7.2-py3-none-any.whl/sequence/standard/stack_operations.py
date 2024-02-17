from typing import List
import copy
import sequence
import sequence.static


# stack ops
@sequence.method("dup")
def duplicate(state: sequence.State, *, deep: bool = False, offset: int = 0):
    """
    Duplicates the item at the top of the stack. There are parameters
    to control if a shallow or deep copy is done, as well as control
    the TOS offset of the item to be duplicated.

    Parameters
    ----------
    [deep]: bool (default: false)
        Controls if the copy is a shallow or deep copy.
    [offset]: int (default: 0)
        The offset (from TOS) of the item you want to duplicate.

    Outputs
    -------
    item_copy: Any
        A copy of the requested item.
    """
    # global _static_copiers
    offset = -1 - offset
    item = state._frame.stack[offset]
    item_type = type(item)
    if item_type in sequence.static.copiers:
        return sequence.static.copiers[item_type](item, deep)
    else:
        if deep:
            return copy.deepcopy(item)
        else:
            return copy.copy(item)


@sequence.method("swap")
def swap(state: sequence.State, *, order: list = [1, 0]):
    """
    Swaps the order of the items at the top of the stack.

    Parameters
    ----------
    [order]: list (default: [1, 0])
        The new order of the TOS. The first integer in the list is TOS
        offset of the item that should be moved to the TOS. The length
        of the list controls the number of items that are reordered.
    """
    size = len(order)
    items = state.popn(size)
    new_items = [items[size-1-i] for i in reversed(order)]
    return tuple(new_items)


@sequence.method("drop")
def drop(state: sequence.State):
    """
    Drops the item at the top of the stack.
    """
    state.pop()


@sequence.method("size")
def stack_size(state: sequence.State):
    """
    Returns the current size (depth) of the stack.

    Outputs
    -------
    stack_size: int
        The size of the stack.
    """
    return len(state._frame.stack)


@sequence.method("pack")
def pack_(state: sequence.State, *, n: int, forward: bool = True, keys: List[str] = None):
    """
    Packs N items from the top of the stack into a single array at the top of
    the stack.

    Parameters
    ----------
    n: int
        The number of items at the top of the stack to pack into the array.
    [forward]: bool (default: true)
        If false, the items are packed in reverse order.
    [keys]: list
        If provided, the items are packed as key-value pairs. The last key
        applies to the TOS item.

    Inputs
    ------
    ...: Any
        n items are consumed from the top of the stack.

    Outputs
    -------
    arr: Array
        An array of items.
    """
    items = list(state.popn(n))
    if not forward:
        items.reverse()
    if keys is not None:
        items = {k: v for k, v in zip(keys, items)}
    return items


@sequence.method("unpack")
def unpack_(state: sequence.State, *, keys: List[str] = None):
    """
    Packs N items from the top of the stack into a single array at the top of
    the stack.

    Parameters
    ----------
    [keys]: list
        Required to unpack a list of key-value pairs. The last key refers to the
        new TOS item.

    Outputs
    -------
    ...: Any
        The unpacked items.
    """
    items = state.pop()
    if keys is not None:
        items = [items[k] for k in keys]
    return tuple(items)
