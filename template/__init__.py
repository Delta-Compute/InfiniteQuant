# The MIT License (MIT)
# Copyright © 2024 Delta Prop Shop LLC
# developer: Delta-Compute
# Copyright © 2024 Delta Prop Shop LLC

__version__ = "1.0.0"
version_split = __version__.split(".")
__spec_version__ = (1000 * int(version_split[0])) + (10 * int(version_split[1])) + (1 * int(version_split[2]))

# Import all submodules.
from . import protocol  # noqa: E402, F401