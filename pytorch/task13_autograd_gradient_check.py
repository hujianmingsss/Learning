import torch


X = torch.tensor(
    [
        [1.0, 2.0],
        [2.0, 0.0],
        [3.0, 1.0],
        [0.0, 2.0],
    ],
    dtype=torch.float64,
)

y_true = torch.tensor(
    [1.0, 4.0, 6.0, -1.0],
    dtype=torch.float64,
)

w = torch.tensor(
    [0.0, 0.0],
    dtype=torch.float64,
    requires_grad=True,
)

b = torch.tensor(
    0.0,
    dtype=torch.float64,
    requires_grad=True,
)


# 1. 前向预测：按照 y_pred = X @ w + b 补全
y_pred = X @ w + b
# 2. MSE：按照 mean((y_true - y_pred) ** 2) 补全
loss = torch.mean((y_true - y_pred) ** 2)

print("backward前w.grad =", w.grad)
print("backward前b.grad =", b.grad)

loss.backward()

grad_w = w.grad.detach().clone()
grad_b = b.grad.detach().clone()

print("backward后w.grad =", w.grad)
print("backward后b.grad =", b.grad)

learning_rate = 0.1

with torch.no_grad():
    w -= learning_rate * grad_w
    b -= learning_rate * grad_b

y_pred_after = X @ w + b
loss_after = torch.mean((y_true - y_pred_after) ** 2)

print("更新后w =", w)
print("更新后b =", b)
print("更新前loss =", loss)
print("更新后loss =", loss_after)
print("清零前w.grad =", w.grad)
print("清零前b.grad =", b.grad)

w.grad.zero_()
b.grad.zero_()

print("清零后w.grad =", w.grad)
print("清零后b.grad =", b.grad)