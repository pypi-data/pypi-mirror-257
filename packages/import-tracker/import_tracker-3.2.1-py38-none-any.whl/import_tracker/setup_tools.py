"""
This module holds tools for libraries to use when definint requirements and
extras_require sets in a setup.py
"""

# Standard
from functools import reduce
from typing import Dict, Iterable, List, Optional, Tuple, Union
import os
import re
import sys

# Local
from .constants import INFO_OPTIONAL
from .import_tracker import track_module
from .log import log

## Public ######################################################################


def parse_requirements(
    requirements: Union[List[str], str],
    library_name: str,
    extras_modules: Optional[List[str]] = None,
    full_depth: bool = True,
    keep_optional: Union[bool, Dict[str, List[str]]] = False,
    **kwargs,
) -> Tuple[List[str], Dict[str, List[str]]]:
    """This helper uses the lists of required modules and parameters for the
    given library to produce requirements and the extras_require dict.

    Args:
        requirements:  Union[List[str], str]
            The list of requirements entries, or a file path pointing to a
            requirements file
        library_name:  str
            The top-level name of the library package
        extras_modules:  Optional[List[str]]
            List of module names that should be used to generate extras_require
            sets
        full_depth:  bool
            Passthrough to track_module. The default here is switched to True so
            that modules which are both direct and transitive dependencies of
            the library are correctly allocated.
        keep_optional:  Union[bool, Dict[str, List[str]]]
            Indicate which optional dependencies should be kept when computing
            the extras sets. If True, all optional dependencies will be kept. If
            False, none will be kept. Otherwise, the argument should be a dict
            mapping known optional dependencies of specific modules that should
            be kept and all optional dependencies not represented in the dict
            will be dropped.
        **kwargs:
            Additional keyword arguments to pass through to track_module

    Returns:
        requirements:  List[str]
            The list of requirements to pass to setup()
        extras_require:  Dict[str, List[str]]
            The extras_require dict to pass to setup()
    """

    # Load all requirements from the requirements file
    if isinstance(requirements, str):
        with open(requirements, "r") as handle:
            requirements_lines = list(handle.readlines())
    elif not isinstance(requirements, (list, tuple, set)):
        raise ValueError(
            f"Invalid type for requirements. Expected str (file) or List. Got {type(requirements)}"
        )
    else:
        requirements_lines = requirements
    requirements = {
        _standardize_package_name(_REQ_SPLIT_EXPR.split(line, 1)[0]): line.strip()
        for line in requirements_lines
        if line.strip() and not line.startswith("#")
    }
    log.debug("Requirements: %s", requirements)

    # Get the set of required modules for each of the listed extras modules
    library_import_mapping = track_module(
        library_name,
        submodules=True,
        detect_transitive=True,
        full_depth=full_depth,
        show_optional=True,
        **kwargs,
    )
    log.debug4("Library Import Mapping:\n%s", library_import_mapping)

    # Remove any unwanted optional imports
    if keep_optional is not True:
        keep_optional = keep_optional or {}
        log.debug2("Trimming optional deps (keep: %s)", keep_optional)
        library_import_mapping = {
            mod_name: {
                dep_name: dep_info
                for dep_name, dep_info in deps_info.items()
                if (
                    not dep_info[INFO_OPTIONAL]
                    or dep_name in keep_optional.get(mod_name, [])
                )
            }
            for mod_name, deps_info in library_import_mapping.items()
        }
        log.debug4("Trimmed Import Mapping:\n%s", library_import_mapping)

    # If no extras_modules are given, track them all
    if not extras_modules:
        extras_modules = list(library_import_mapping.keys())
    log.debug2("Tracking extras modules: %s", extras_modules)

    # Get a mapping from all known imports to their requirement names
    requirement_name_map = {}
    for imports in library_import_mapping.values():
        for import_name in imports:
            if import_name not in requirement_name_map:
                requirement_name_map[import_name] = _get_required_packages_for_imports(
                    [import_name]
                )[0]
    log.debug3("Requirement Name Map: %s", requirement_name_map)

    # Get the import sets for each requested extras
    missing_extras_modules = [
        mod for mod in extras_modules if mod not in library_import_mapping
    ]
    assert (
        not missing_extras_modules
    ), f"No tracked imports found for: {missing_extras_modules}"
    import_sets = {
        mod_name: {requirement_name_map[import_name] for import_name in imports}
        for mod_name, imports in library_import_mapping.items()
    }
    log.debug("Import sets: %s", import_sets)

    # Determine the common requirements as the intersection of all extras sets
    # union'ed with all other import sets
    common_intersection = None
    non_extra_union = set()
    for import_set_name, import_set in import_sets.items():
        if common_intersection is None:
            common_intersection = import_set
        else:
            common_intersection = common_intersection.intersection(import_set)

        # Determine if this import set falls outside of the extras
        import_set_parts = import_set_name.split(".")
        in_extra = any(
            extras_module.startswith(import_set_name)
            for extras_module in extras_modules
        )
        if not in_extra:
            for i in range(len(import_set_parts)):
                parent_path = ".".join(import_set_parts[: i + 1])
                if parent_path in extras_modules:
                    in_extra = True
                    break
        if not in_extra:
            log.debug3(
                "%s not covered by an extra. Adding %s to non extra union",
                import_set_name,
                import_set,
            )
            non_extra_union = non_extra_union.union(import_set)
    common_intersection = common_intersection or set()
    if len(extras_modules) == 1:
        common_intersection = set()
    log.debug3("Raw common intersection: %s", common_intersection)

    common_imports = common_intersection.union(non_extra_union)
    log.debug3("Common intersection: %s", common_intersection)
    log.debug3("Non extra union: %s", non_extra_union)
    log.debug("Common Imports: %s", common_imports)

    # Compute the sets of unique requirements for each tracked module
    extras_require_sets = {
        set_name: import_set - common_imports
        for set_name, import_set in import_sets.items()
        if set_name in extras_modules
    }
    log.debug("Extras require sets: %s", extras_require_sets)

    # Add any listed requirements in that don't show up in any tracked module.
    # These requirements may be needed by an untracked portion of the library or
    # they may be runtime imports.
    all_tracked_requirements = reduce(
        lambda acc_set, req_set: acc_set.union(req_set),
        extras_require_sets.values(),
        common_imports,
    )
    missing_reqs = (
        set(_get_required_packages_for_imports(requirements.keys()))
        - all_tracked_requirements
    )
    log.debug(
        "Adding missing requirements %s to common_imports",
        sorted(list(missing_reqs)),
    )
    common_imports = common_imports.union(missing_reqs)

    # Add a special "all" group to the extras_require that will install all deps
    # needed for all extras
    if _ALL_GROUP not in extras_require_sets:
        all_reqs = all_tracked_requirements.union(missing_reqs)
        log.debug("Adding [%s] requirement group: %s", _ALL_GROUP, all_reqs)
        extras_require_sets[_ALL_GROUP] = all_reqs

    # Map all dependencies through those listed in requirements.txt
    standardized_requirements = {
        key.replace("-", "_"): val for key, val in requirements.items()
    }
    return sorted(_map_requirements(standardized_requirements, common_imports)), {
        set_name: _map_requirements(standardized_requirements, import_set)
        for set_name, import_set in extras_require_sets.items()
    }


## Implementation Details ######################################################

# Regex for parsing requirements
_REQ_SPLIT_EXPR = re.compile(r"[=><!~\[]")

# Exprs for finding module names
_PKG_VERSION_EXPR = re.compile("-[0-9]")
_PKG_NAME_EXPR = re.compile("^Name: ([^ \t\n]+)")

# Extras require group name for the union of all dependencies
_ALL_GROUP = "all"

# Lazily created global mapping from module name to package name
_MODULE_TO_PKG = None


def _map_requirements(declared_dependencies, dependency_set):
    """Given the declared dependencies from requirements.txt and the given
    programmatic dependency set, return the subset of declared dependencies that
    matches the dependency set
    """
    return sorted(
        [
            declared_dependencies[dep.replace("-", "_")]
            for dep in dependency_set
            if dep.replace("-", "_") in declared_dependencies
        ]
    )


def _map_modules_to_package_names():
    """Look for any information we can get to map from the name of the imported
    module to the name of the package that installed that module.

    WARNING: This is a best-effort function! It attempts to look for common
        conventions from pip, but it's very possible to break this function by
        non-standard installation topology.
    """
    modules_to_package_names = {}
    for path_dir in sys.path:

        # Traverse all "RECORD" files holding records of the pip installations
        for root, dirs, files in os.walk(path_dir):
            if "RECORD" in files:

                # Parse the package name from the info file name
                package_file = os.path.relpath(root, path_dir).split("/")[-1]
                package_name = _PKG_VERSION_EXPR.split(package_file)[0]

                # Look for a more accurate package name in METADATA. This can
                # fix the case where the actual package uses a '-' but the wheel
                # uses an '_'.
                if "METADATA" in files:
                    md_file = os.path.join(root, "METADATA")
                    # Parse the package name from the metadata file
                    with open(md_file, "r") as handle:
                        for line in handle.readlines():
                            match = _PKG_NAME_EXPR.match(line.strip())
                            if match:
                                package_name = match.group(1)
                                break

                # Iterate each line in RECORD and look for lines that look like
                # unpacking python modules
                with open(os.path.join(root, "RECORD"), "r") as handle:
                    for modname in map(
                        lambda mn: os.path.splitext(mn)[0],
                        filter(
                            lambda mn: (
                                mn
                                and mn != "__pycache__"
                                and os.path.splitext(mn)[-1]
                                not in [".pth", ".dist-info", ".egg-info"]
                                and "." not in mn
                            ),
                            {
                                line.split("/")[0].split(",")[0].strip()
                                for line in handle.readlines()
                            },
                        ),
                    ):
                        modules_to_package_names.setdefault(modname, set()).add(
                            _standardize_package_name(package_name)
                        )

    return modules_to_package_names


def _standardize_package_name(raw_package_name):
    """Helper to convert the arbitrary ways packages can be represented to a
    common (matchable) representation
    """
    return raw_package_name.strip().lower().replace("-", "_")


def _get_required_packages_for_imports(imports: Iterable[str]) -> List[str]:
    """Get the set of installable packages required by this list of imports"""
    # Lazily create the global mapping
    global _MODULE_TO_PKG
    if _MODULE_TO_PKG is None:
        _MODULE_TO_PKG = _map_modules_to_package_names()

    # Merge the required packages for each
    required_pkgs = set()
    for mod in imports:
        # If there is a known mapping, use it
        if mod in _MODULE_TO_PKG:
            required_pkgs.update(_MODULE_TO_PKG[mod])

        # Otherwise, assume that the name of the module is itself the name of
        # the package
        else:
            required_pkgs.add(mod)
    return sorted(list(required_pkgs))
