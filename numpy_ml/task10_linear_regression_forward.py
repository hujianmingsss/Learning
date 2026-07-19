from __future__ import annotations

import numpy as np


def linear_predict(
    X: np.ndarray,
    w: np.ndarray,
    b: float,
) -> np.ndarray:
    y_pred = X @ w + b
    return y_pred

def mean_squared_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    error = y_true - y_pred
    squared_error = error ** 2
    mse = np.mean(squared_error)
    return float(mse)

if __name__ == "__main__":
    X = np.array([
        [1.0, 2.0],
        [2.0, 0.0],
        [3.0, 1.0],
        [0.0, 2.0],
    ])

    w = np.array([2.0, -1.0])
    b = 0.5

    y_pred = linear_predict(X, w, b)
    y_true = np.array([1.0, 4.0, 6.0, -1.0])

    mse = mean_squared_error(y_true, y_pred)
    
    expected_y_pred = np.array([0.5, 4.5, 5.5, -1.5])
    expected_mse = 0.25

    print(
        "预测结果是否正确：",
        np.allclose(y_pred, expected_y_pred), #allclose近似相等
    )
    
    # np.allclose()
    # → 比较两个数组中的所有元素是否近似相等

    # np.isclose()
    # → 比较两个标量是否近似相等
    print(
        "MSE是否正确：",
        np.isclose(mse, expected_mse), #isclose是否近似相等
    )

    print("X.shape =", X.shape)
    print("w.shape =", w.shape)
    print("y_pred.shape =", y_pred.shape)
    print("y_pred =", y_pred)
    print("mse =", mse)
