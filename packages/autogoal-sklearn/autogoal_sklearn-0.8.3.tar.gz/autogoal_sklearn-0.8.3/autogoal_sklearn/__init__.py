"""
This module contains wrappers for several estimators and transformers
from `scikit-learn`.

!!! warning
    Importing this module requires `sklearn` with a version equal or greater
    than `0.22`. You can either install it manually or with `pip install autogoal[sklearn]`.

Most of the classes and functions inside this module deal with the automatic
generation of wrappers and thus are considered private API.

The main public functionality exposed by this module is the function
[find_classes](/api/autogoal_sklearn/#find_classes), which allows to
enumerate the wrappers implemented in this module applying some filters.

!!! note
    You can manually import any wrapper class directly from `autogoal_sklearn._generated`
    buy beware that namespace changes wildly from version to version and classes in it
    might disappear or change their signature anytime.
"""

try:
    import sklearn

    major, minor, *rest = sklearn.__version__.split(".")
    assert (int(major) == 0 and int(minor) >= 22) or int(major) > 0
except:
    print("(!) Code in `autogoal_sklearn` requires `sklearn=^0.22`.")
    print("(!) You can install it with `pip install autogoal[sklearn]`.")
    raise ImportError()


# Filter out sklearn convergence and joblib warnings
import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", message=".*resource_tracker.*")
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", module="sklearn")
warnings.filterwarnings("ignore", module="scipy")
warnings.filterwarnings("ignore", module="numpy")


from autogoal_sklearn._generated import *
from autogoal_sklearn._manual import *
