from __future__ import annotations

import numpy as np

from task10_linear_regression_forward import (
    linear_predict,
    mean_squared_error,
)


def mse_gradients(
    X: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> tuple[np.ndarray, float]:
    error = y_pred - y_true
    n = X.shape[0]
    grad_w = (2/n) * np.transpose(X) @ error
    grad_b = (2/n) * np.sum(error)
    return grad_w, float(grad_b)

def gradient_descent_step(
    w: np.ndarray,
    b: float,
    grad_w: np.ndarray,
    grad_b: float,
    learning_rate: float,
) -> tuple[np.ndarray, float]:
    w_new = w - learning_rate * grad_w
    b_new = b - learning_rate * grad_b
    return w_new, float(b_new)

if __name__ == "__main__":
    X = np.array([
        [1.0, 2.0],
        [2.0, 0.0],
        [3.0, 1.0],
        [0.0, 2.0],
    ])

    y_true = np.array([1.0, 4.0, 6.0, -1.0])

    w = np.array([0.0, 0.0])
    b = 0.0

    y_pred_before = linear_predict(X, w, b)
    loss_before = mean_squared_error(y_true, y_pred_before)

    grad_w, grad_b = mse_gradients(
        X,
        y_true,
        y_pred_before,
    )
    learning_rate = 0.1

    w_new, b_new = gradient_descent_step(
        w,
        b,
        grad_w,
        grad_b,
        learning_rate,
    )
    print("w_new =", w_new)
    print("b_new =", b_new)
    print("y_pred_before =", y_pred_before)
    print("loss_before =", loss_before)
    print("grad_w =", grad_w)
    print("grad_b =", grad_b)
    
    y_pred_after = linear_predict(X, w_new, b_new)
    loss_after = mean_squared_error(y_true, y_pred_after)
    print("y_pred_after =", y_pred_after)
    print("loss_after =", loss_after)
    print("loss下降 =", loss_after < loss_before)

    print(
        "更新后的w是否正确：",
        np.allclose(w_new, np.array([1.35, 0.3])),
    )
    print(
        "更新后的b是否正确：",
        np.isclose(b_new, 0.5),
    )
    print(
        "更新后的loss是否正确：",
        np.isclose(loss_after, 2.11875),
    )