import pytest
import synthetic_generator as synthetic_generator

import types
from typing import Set, Tuple, Type


def submodule_classes_info(module: types.ModuleType) -> Tuple[Set[str], Set[Type]]:
    """
    List all class names and class objects defined in the given module.

    Args:
        module (types.ModuleType): The module from which to extract class names and class objects.

    Returns:
        tuple: A tuple containing:
            - A set of class names (as strings) defined in the module.
            - A set of class objects (types) defined in the module.
    """
    name = module.__name__
    classes, objects = synthetic_generator.utils.get_classes(module)
    print(f"Module {name} - Contains {len(classes)} classes")
    for cls, obj in zip(classes, objects):
        print("\t-> {: <30} : id = {}".format(cls, hex(id(obj))))
    return classes, objects


if __name__ == "__main__":
    print(f'`main` block at file "{__file__}"')

    submodule_classes_info(synthetic_generator.attribute)
submodule_classes_info(synthetic_generator.dtype)
