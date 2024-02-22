# Import the main class from the miner module
from .categorical_woe import woe_discrete as categorical_woe
from .continuous_binning_woe import continuous_binning as continuous_woe

# Optionally define an __all__ for explicitness on what is exported
__all__ = ['categorical_woe','continuous_woe']