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
    [
        [1.0],
        [4.0],
        [6.0],
        [-1.0],
    ],
    dtype=torch.float64,
)


class LinearRegressionModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = torch.nn.Linear(
            2, 1, dtype = torch.float64,
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        # 3. 调用 self.linear 完成前向计算
        return self.linear(X)
    
def train_model(
    model: torch.nn.Module,
    X: torch.Tensor,
    y_true: torch.Tensor,
    learning_rate: float,
    num_steps: int,
) -> list[float]:

    criterion = torch.nn.MSELoss()

    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=learning_rate,
    )

    loss_history = []

    model.train()

    for _ in range(num_steps):
        optimizer.zero_grad(set_to_none=True)

        y_pred = model(X)

        if y_pred.shape != y_true.shape:
            raise ValueError(
                f"shape不一致：y_pred={y_pred.shape}, "
                f"y_true={y_true.shape}"
            )

        loss = criterion(y_pred, y_true)
        loss_history.append(loss.item())

        loss.backward()
        optimizer.step()
    model.eval()

    with torch.no_grad():
        final_y_pred = model(X)

        if final_y_pred.shape != y_true.shape:
            raise ValueError(
                f"shape不一致：final_y_pred={final_y_pred.shape}, "
                f"y_true={y_true.shape}"
            )

        final_loss = criterion(final_y_pred, y_true)
        loss_history.append(final_loss.item())

    return loss_history

model = LinearRegressionModel()

with torch.no_grad():
    model.linear.weight.zero_()
    model.linear.bias.zero_()

loss_history = train_model(
    model=model,
    X=X,
    y_true=y_true,
    learning_rate=0.1,
    num_steps=50,
)

loss_is_monotonic = all(
    loss_history[index + 1] <= loss_history[index] + 1e-12
    for index in range(len(loss_history) - 1)
)

print("损失单调不增 =", loss_is_monotonic)

if not loss_is_monotonic:
    raise AssertionError("训练损失没有保持单调不增")

wrong_y = y_true.squeeze(1)

print("wrong_y.shape =", wrong_y.shape)

wrong_model = LinearRegressionModel()

with torch.no_grad():
    wrong_model.linear.weight.zero_()
    wrong_model.linear.bias.zero_()

try:
    train_model(
        model=wrong_model,
        X=X,
        y_true=wrong_y,
        learning_rate=0.1,
        num_steps=1,
    )
except ValueError as error:
    print("捕获到预期异常：", error)
else:
    raise AssertionError("错误shape未被train_model拒绝")

loss_is_monotonic = all(
    loss_history[index + 1] <= loss_history[index] + 1e-12
    for index in range(len(loss_history) - 1)
)

print("损失单调不增 =", loss_is_monotonic)

if not loss_is_monotonic:
    raise AssertionError("训练损失没有保持单调不增")
print("loss_history长度 =", len(loss_history))
print("第一次损失 =", loss_history[0])
print("最终参数 =", model.linear.weight, model.linear.bias)
print("最终损失 =", loss_history[-1])

#单步实现
# model = LinearRegressionModel()

# with torch.no_grad():
#     model.linear.weight.zero_()
#     model.linear.bias.zero_()

# print("weight =", model.linear.weight)
# print("bias =", model.linear.bias)
# print("weight.shape =", model.linear.weight.shape)
# print("bias.shape =", model.linear.bias.shape)

# y_pred = model(X)

# print("y_pred.shape =", y_pred.shape)

# for name, parameter in model.named_parameters():
#     print(
#         "参数名 =", name,
#         "shape =", parameter.shape,
#         "requires_grad =", parameter.requires_grad,
#     )

# print("state_dict键 =", list(model.state_dict().keys()))

# parameter_count = sum(
#     parameter.numel() for parameter in model.parameters()#生成器表达式
# )
# print("参数总数 =", parameter_count)

# criterion = torch.nn.MSELoss()

# optimizer = torch.optim.SGD(
#     model.parameters(),
#     lr = 0.1,
# )

# optimizer.zero_grad(set_to_none=True)
# y_pred = model(X)

# if y_pred.shape != y_true.shape:
#     raise ValueError(
#         f"shape不一致：y_pred={y_pred.shape}, "
#         f"y_true={y_true.shape}"
#     )

# loss = criterion(y_pred, y_true)

# print("initial loss =", loss.item())

# loss.backward()

# print("weight.grad =", model.linear.weight.grad)
# print("bias.grad =", model.linear.bias.grad)

# optimizer.step()

# print("updated weight =", model.linear.weight)
# print("updated bias =", model.linear.bias)

# with torch.no_grad():
#     y_pred_after = model(X)
#     loss_after = criterion(y_pred_after, y_true)

# print("loss after one step =", loss_after.item())

