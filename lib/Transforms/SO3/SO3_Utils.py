from lib.Transforms.SO3 import SO3
from lib.Transforms.so3.so3 import so3
from lib.Transforms.conversions.conversions import SO3_to_log, log_to_SO3
import numpy as np

# Log of S centered in R
centered_log_map = lambda S, R: SO3_to_log(S @ R.inverse())


def SO3_median(rotation_list: list, threshold=1e-6, S_t=None):
    # We provide S_t as a first guess
    assert S_t is not None

    for _ in range(100):
        # Center the elements on the current estimate
        elements = np.array(
            [centered_log_map(x, S_t).w for x in rotation_list]
        )
        numerator = 0
        denumerator = 0
        for xi in elements:
            X = np.linalg.norm(xi)
            numerator += xi / X
            denumerator += 1 / X
        delta = numerator / denumerator
        S_t = log_to_SO3(so3(delta)) @ S_t

        if np.linalg.norm(delta) < threshold:
            break

    return S_t


def SO3_mean(rotations):
    # Correct ?
    v_is = np.array([SO3_to_log(x).w for x in rotations])
    return log_to_SO3(so3(np.mean(v_is, axis=0)))
