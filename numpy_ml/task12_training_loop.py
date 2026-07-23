import numpy as np
from task10_linear_regression_forward import (
    linear_predict,
    mean_squared_error,
)
from task11_gradient_descent_step import (
    mse_gradients,
    gradient_descent_step,
)
def train_linear_regression(
    X: np.ndarray,
    y_true: np.ndarray,
    initial_w: np.ndarray,
    initial_b: float,
    learning_rate: float,
    num_steps: int,
) -> tuple[np.ndarray, float, list[float]]:
    w = initial_w.copy()
    b = float(initial_b)
    loss_history: list[float] = []

    for _ in range(num_steps):
        # 前向传播
        y_pred = linear_predict(X, w, b)

        # 计算并记录当前损失
        loss = mean_squared_error(y_true, y_pred)
        loss_history.append(loss)

        # 反向传播：计算梯度
        grad_w, grad_b = mse_gradients(
            X,
            y_true,
            y_pred,
        )

        # 更新参数
        w, b = gradient_descent_step(
            w,
            b,
            grad_w,
            grad_b,
            learning_rate,
        )

    # 记录完成全部更新后的最终损失
    final_y_pred = linear_predict(X, w, b)
    final_loss = mean_squared_error(y_true, final_y_pred)
    loss_history.append(final_loss)

    return w, b, loss_history


if __name__ == "__main__":
    X = np.array([
        [1.0, 2.0],
        [2.0, 0.0],
        [3.0, 1.0],
        [0.0, 2.0],
    ])

    y_true = np.array([1.0, 4.0, 6.0, -1.0])

    initial_w = np.array([0.0, 0.0])
    initial_b = 0.0

    final_w, final_b, loss_history = train_linear_regression(
        X=X,
        y_true=y_true,
        initial_w=initial_w,
        initial_b=initial_b,
        learning_rate=0.1,
        num_steps=50,
    )

    print("loss_history长度 =", len(loss_history))
    print("初始loss =", loss_history[0])
    print("第一次更新后的loss =", loss_history[1])
    print("最终loss =", loss_history[-1])
    print("最终w =", final_w)
    print("最终b =", final_b)
    print("initial_w未修改 =", np.array_equal(initial_w, [0.0, 0.0]))
    
    loss_never_increases = np.all(np.diff(loss_history) <= 0)

    print("loss始终未增加 =", loss_never_increases)
    print("\n学习率对照实验")

    for learning_rate in [0.01, 0.1, 0.5]:
        _, _, current_loss_history = train_linear_regression(
            X=X,
            y_true=y_true,
            initial_w=initial_w,
            initial_b=initial_b,
            learning_rate=learning_rate,
            num_steps=50,
        )

        print(f"\nlearning_rate = {learning_rate}")
        print("初始loss =", current_loss_history[0])
        print("最终loss =", current_loss_history[-1])
        print(
            "最终loss小于初始loss =",
            current_loss_history[-1] < current_loss_history[0],
        )