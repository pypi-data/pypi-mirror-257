import abc
import datetime
import inspect
import re
import textwrap
import warnings
from pathlib import Path
from typing import Tuple

import black
import enlighten
import numpy as np
import sklearn
import sklearn.cluster
import sklearn.cross_decomposition
import sklearn.feature_extraction
import sklearn.impute
import sklearn.naive_bayes
from joblib import parallel_backend
from numpy import inf, nan
from sklearn.datasets import make_classification

from autogoal import kb
from autogoal_sklearn._utils import get_input_output, is_algorithm
from autogoal.grammar import (
    BooleanValue,
    CategoricalValue,
    ContinuousValue,
    DiscreteValue,
)
from autogoal.kb import (
    AlgorithmBase,
    Tensor,
    Continuous,
    Categorical,
    Dense,
    Discrete,
    Sparse,
)
from autogoal.utils import nice_repr

# try:
#     import dask
#     from dask.distributed import Client

#     DASK_CLIENT = Client(processes=False)
#     PARALLEL_BACKEND = 'dask'
# except ImportError:
# PARALLEL_BACKEND = 'loky'


@nice_repr
class SklearnWrapper(AlgorithmBase):
    def __init__(self):
        self._mode = "train"
        self._fixed = False
        
    def reset(self):
        try:
            self.__init__(**self.init_params)
        except Exception as e:
            pass
        
    @classmethod
    def is_upscalable(cls) -> bool:
        a = hasattr(cls, "partial_fit")
        return a

    def train(self):
        self._mode = "train"

    def eval(self):
        self._mode = "eval"

    def run(self, *args):
        if self._mode == "train":
            return self._train(*args)
        elif self._mode == "eval":
            return self._eval(*args)

        raise ValueError("Invalid mode: %s" % self._mode)

    @abc.abstractmethod
    def _train(self, *args):
        pass

    @abc.abstractmethod
    def _eval(self, *args):
        pass


class SklearnEstimator(SklearnWrapper):
    def _train(self, X, y=None):
        # if self._fixed:
        #     self.reset()
        #     self._fixed = False
        
        self.fit(X, y)
        
        # if hasattr(self, "partial_fit"):
        #     self.partial_fit(X, y, np.unique(y))
        # else:
        return y

    def _eval(self, X, y=None):
        self._fixed = True
        return self.predict(X)

    @abc.abstractmethod
    def fit(self, X, y):
        pass

    @abc.abstractmethod
    def predict(self, X):
        pass


class SklearnTransformer(SklearnWrapper):
    def _train(self, X, y=None):
        if hasattr(self, "partial_fit"):
            self.partial_fit(X)
            return self.transform(X)
        else:
            return self.fit_transform(X)

    def _eval(self, X, y=None):
        return self.transform(X)

    @abc.abstractmethod
    def fit_transform(self, X, y=None):
        pass

    @abc.abstractmethod
    def transform(self, X, y=None):
        pass


TYPE_ALIASES = {
    Tensor[1, None, None]: "Vector",
    Tensor[1, Continuous, None]: "VectorContinuous",
    Tensor[1, Categorical, Dense]: "VectorCategorical",
    Tensor[1, Discrete, Dense]: "VectorDiscrete",
    Tensor[2, None, None]: "Matrix",
    Tensor[2, Continuous, None]: "MatrixContinuous",
    Tensor[2, Continuous, Dense]: "MatrixContinuousDense",
    Tensor[2, Continuous, Sparse]: "MatrixContinuousSparse",
    Tensor[2, Categorical, Dense]: "MatrixCategorical",
    Tensor[2, Discrete, Dense]: "MatrixDiscrete",
    Tensor[3, Continuous, Dense]: "Tensor3",
    Tensor[4, Continuous, Dense]: "Tensor4",
}


GENERATION_RULES = dict(
    LatentDirichletAllocation=dict(ignore_params=set(["evaluate_every"])),
    RadiusNeighborsClassifier=dict(
        ignore=True,
    ),
    KNeighborsTransformer=dict(ignore_params=set(["metric"])),
    RadiusNeighborsTransformer=dict(ignore_params=set(["metric"])),
    LocalOutlierFactor=dict(ignore_params=set(["metric"])),
    RadiusNeighborsRegressor=dict(ignore_params=set(["metric"])),
    LabelBinarizer=dict(
        ignore_params=set(["neg_label", "pos_label"]),
        input_annotation=kb.Seq[kb.Label],
    ),
    HashingVectorizer=dict(
        ignore_params=set(["token_pattern", "analyzer", "input", "decode_error"])
    ),
    SpectralBiclustering=dict(ignore_params=set(["n_components", "n_init"])),
    SpectralCoclustering=dict(ignore_params=set(["n_init"])),
    KMeans=dict(ignore_params=set(["n_init"])),
    MiniBatchKMeans=dict(ignore_params=set(["batch_size", "n_init"])),
    DictionaryLearning=dict(ignore=True),
    MiniBatchDictionaryLearning=dict(ignore=True),
    LassoLars=dict(ignore_params=["alpha"]),
    TheilSenRegressor=dict(ignore_params=["max_subpopulation"]),
    TSNE=dict(ignore=True, ignore_params=["perplexity"]),
)


def build_sklearn_wrappers():
    imports = _walk(sklearn)

    manager = enlighten.get_manager()
    counter = manager.counter(total=len(imports), unit="classes")

    path = Path(__file__).parent / "_generated.py"

    with open(path, "w") as fp:
        fp.write(
            textwrap.dedent(
                f"""
            # AUTOGENERATED ON {datetime.datetime.now()}
            ## DO NOT MODIFY THIS FILE MANUALLY

            from numpy import inf, nan

            from autogoal.grammar import ContinuousValue, DiscreteValue, CategoricalValue, BooleanValue
            from autogoal_sklearn._builder import SklearnEstimator, SklearnTransformer
            from autogoal.kb import *
            """
            )
        )

        for cls in imports:
            counter.update()
            _write_class(cls, fp)

    black.reformat_one(
        path, True, black.WriteBack.YES, black.FileMode(), black.Report()
    )

    counter.close()
    manager.stop()


def _write_class(cls, fp):
    rules = GENERATION_RULES.get(cls.__name__, {})

    if rules.get("ignore"):
        return

    ignore_args = rules.get("ignore_params", [])

    print("Generating class: %r" % cls)

    args = _get_args(cls)

    for a in ignore_args:
        args.pop(a, None)

    args = _get_args_values(cls, args)
    inputs, outputs = get_input_output(cls)
    inputs = rules.get("input_annotation", inputs)
    outputs = rules.get("output_annotation", outputs)

    if not inputs:
        warnings.warn("Cannot find correct types for %r" % cls)
        return

    s = " " * 4
    args_str = f",\n{s * 4}".join(f"{key}: {value}" for key, value in args.items())
    init_str = f",\n{s * 5}".join(f"{key}={key}" for key in args)
    init_params_dict_str = "{" + ", ".join(f"'{key}':{key}" for key in args) + "}"

    output_str = TYPE_ALIASES.get(outputs) or repr(outputs)

    base_class = (
        "SklearnEstimator" if is_algorithm(cls) == "estimator" else "SklearnTransformer"
    )

    input_str = "input: " + (TYPE_ALIASES.get(inputs) or repr(inputs))
    run_input_str = "input"
    if type(inputs) == tuple:
        if len(inputs) > 2:
            raise Exception(
                "Unsuported input string representation for algorithms with more than 2 input elements."
            )
        x, y = inputs
        input_str = f"X: {TYPE_ALIASES.get(x) or repr(x)}, y: Supervised[{TYPE_ALIASES.get(y) or repr(y)}]"
        run_input_str = "X, y"

    fp.write(
        textwrap.dedent(
            f"""
        from {cls.__module__} import {cls.__name__} as _{cls.__name__}

        class {cls.__name__}(_{cls.__name__}, {base_class}):
            def __init__(
                self,
                {args_str}
            ):
                {base_class}.__init__(self)
                _{cls.__name__}.__init__(
                    self,
                    {init_str}
                )
                self.init_params = {init_params_dict_str}

            def run(self, {input_str}) -> {output_str}:
               return {base_class}.run(self, {run_input_str})
        """
        )
    )

    print("Successfully generated" + cls.__name__)
    fp.flush()


def _is_algorithm(cls, verbose=False):
    if hasattr(cls, "fit"):
        return True
    else:
        if verbose:
            warnings.warn("%r doesn't have `fit`" % cls)

    if hasattr(cls, "transform"):
        return True
    else:
        if verbose:
            warnings.warn("%r doesn't have `transform`" % cls)

    return False


def _walk(module):
    imports = set()

    def _walk_p(module, visited):
        if module in visited:
            return

        visited.add(module)
        all_classes = inspect.getmembers(module, inspect.isclass)

        for name, obj in all_classes:
            if obj in imports:
                continue

            try:
                if not "sklearn" in inspect.getfile(obj):
                    continue

                print(obj)

                if isinstance(obj, type):
                    if name.endswith("CV"):
                        continue

                    if not _is_algorithm(obj):
                        continue

                    imports.add(obj)

            except Exception as e:
                print(repr(e))

        for name, inner_module in inspect.getmembers(module, inspect.ismodule):
            if not "sklearn" in inspect.getfile(module):
                continue

            print(inner_module)
            _walk_p(inner_module, visited)

    _walk_p(module, set())

    imports = sorted(imports, key=lambda c: (c.__module__, c.__name__))

    print("Finally found classes:")

    for cls in imports:
        print(cls)

    return imports


def _find_parameter_values(parameter, cls):
    documentation = []
    lines = cls.__doc__.split("\n")

    while lines:
        l = lines.pop(0)
        if l.strip().startswith(parameter):
            documentation.append(l)
            tabs = l.index(parameter)
            break

    while lines:
        l = lines.pop(0)

        if not l.strip():
            continue

        if l.startswith(" " * (tabs + 1)):
            documentation.append(l)
        else:
            break

    options = set(re.findall(r"'(\w+)'", " ".join(documentation)))
    valid = []
    invalid = []
    skip = set(["deprecated", "auto_deprecated", "precomputed"])

    for opt in options:
        opt = opt.lower()

        if opt in skip:
            continue

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if _try(cls, parameter, opt):
                valid.append(opt)
            else:
                invalid.append(opt)

    if valid:
        return CategoricalValue(*sorted(valid))

    return None


X, y = make_classification()


def _try(cls, arg, value):
    try:
        print(f"Trying {cls}({arg}={value})... ", end="")
        cls(**{arg: value}).fit(X, y)
        print("OK")
        return True
    except:
        print("ERROR")
        return False


def _get_args(cls):
    specs = inspect.getfullargspec(cls.__init__)

    args = []
    args += specs.args or []
    args += specs.kwonlyargs or []

    defaults = []
    defaults += specs.defaults or []
    defaults += list((specs.kwonlydefaults or {}).values())

    if not args or not defaults:
        return {}

    args = args[-len(defaults) :]

    args_map = {k: v for k, v in zip(args, defaults)}

    drop_args = [
        "verbose",
        "random_state",
        "n_jobs",
        "max_iter",
        "class_weight",
        "warm_start",
        "copy_X",
        "copy_x",
        "copy",
        "eps",
        "n_init",
    ]

    for arg in drop_args:
        args_map.pop(arg, None)

    print("Found args: %r" % args_map)

    return args_map


def _get_args_values(cls, args_map):
    result = {}

    for arg, value in args_map.items():
        values = _get_arg_values(arg, value, cls)
        if not values:
            continue
        result[arg] = values

    return result


def _get_arg_values(arg, value, cls):
    print(f"Computing valid values for: {arg}={value}")

    try:
        if isinstance(value, bool):
            annotation = BooleanValue()
        elif isinstance(value, int):
            annotation = _get_integer_values(arg, value, cls)
        elif isinstance(value, float):
            annotation = _get_float_values(arg, value, cls)
        elif isinstance(value, str):
            annotation = _find_parameter_values(arg, cls)
        else:
            annotation = None
    except:
        annotation = None

    print(f"Found annotation {arg}:{annotation}")

    return annotation


def _get_integer_values(arg, value, cls):
    if value > 0:
        min_value = 0
        max_value = 2 * value
    elif value == 0:
        min_value = -100
        max_value = 100
    else:
        return None

    # binary search for minimum value
    left = min_value
    right = value

    while left < right:
        current_value = int((left + right) / 2)
        if current_value in [left, right]:
            break

        if _try(cls, arg, current_value):
            right = current_value
        else:
            left = current_value

    min_value = right

    # binary search for maximum value
    left = value
    right = max_value

    while left < right:
        current_value = int((left + right) / 2)
        if current_value in [left, right]:
            break

        if _try(cls, arg, current_value):
            left = current_value
        else:
            right = current_value

    max_value = left

    if min_value < max_value:
        return DiscreteValue(min=min_value, max=max_value)

    return None


def _get_float_values(arg, value, cls):
    if value in [inf, nan]:
        return None

    if value > 0:
        min_value = -10 * value
        max_value = 10 * value
    elif value == 0:
        min_value = -1
        max_value = 1
    else:
        return None

    # binary search for minimum value
    left = min_value
    right = value

    while abs(left - right) > 1e-2:
        current_value = round((left + right) / 2, 3)
        if _try(cls, arg, current_value):
            right = current_value
        else:
            left = current_value

    min_value = right

    # binary search for maximum value
    left = value
    right = max_value

    while abs(left - right) > 1e-2:
        current_value = round((left + right) / 2, 3)
        if _try(cls, arg, current_value):
            left = current_value
        else:
            right = current_value

    max_value = left

    if max_value - min_value >= 2 * value:
        return ContinuousValue(min=min_value, max=max_value)

    return None


if __name__ == "__main__":
    build_sklearn_wrappers()
