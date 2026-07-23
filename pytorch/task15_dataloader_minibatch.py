import torch
from torch.utils.data import DataLoader, TensorDataset


# 9个样本，每个样本有2个特征
X = torch.tensor(
    [
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [2.0, 0.0],
        [0.0, 2.0],
        [2.0, 1.0],
        [1.0, 2.0],
        [2.0, 2.0],
    ],
    dtype=torch.float64,
)

# 标签保持二维形状 (9, 1)
y_true = torch.tensor(
    [
        [0.5],
        [2.5],
        [-0.5],
        [1.5],
        [4.5],
        [-1.5],
        [3.5],
        [0.5],
        [2.5],
    ],
    dtype=torch.float64,
)

# 样本编号只用于检查每个epoch的数据覆盖情况
sample_ids = torch.arange(X.shape[0])

dataset = TensorDataset(sample_ids, X, y_true)

train_loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=False,
    drop_last=False,
    num_workers=0,
)

print("len(dataset) =", len(dataset))
print("len(train_loader) =", len(train_loader))

# 检查DataLoader生成的batch
for batch_index, (batch_ids, batch_X, batch_y) in enumerate(
    train_loader,
    start=1,
):
    print(
        "batch =", batch_index,
        "ids =", batch_ids.tolist(),
        "X.shape =", batch_X.shape,
        "y.shape =", batch_y.shape,
    )


class LinearRegressionModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = torch.nn.Linear(
            in_features=2,
            out_features=1,
            dtype=torch.float64,
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.linear(X)


model = LinearRegressionModel()

# 将模型参数初始化为0
with torch.no_grad():
    model.linear.weight.zero_()
    model.linear.bias.zero_()


def evaluate_full_loss(
    model: torch.nn.Module,
    X: torch.Tensor,
    y_true: torch.Tensor,
    criterion: torch.nn.Module,
) -> float:
    model.eval()

    with torch.no_grad():
        y_pred = model(X)

        if y_pred.shape != y_true.shape:
            raise ValueError(
                f"shape不一致："
                f"y_pred={y_pred.shape}, "
                f"y_true={y_true.shape}"
            )

        loss = criterion(y_pred, y_true)

    return loss.item()


criterion = torch.nn.MSELoss()

initial_full_loss = evaluate_full_loss(
    model,
    X,
    y_true,
    criterion,
)

print("initial_full_loss =", initial_full_loss)


def train_minibatch(
    model: torch.nn.Module,
    train_loader: DataLoader,
    X: torch.Tensor,
    y_true: torch.Tensor,
    learning_rate: float,
    num_epochs: int,
) -> tuple[list[float], list[float], list[int]]:

    criterion = torch.nn.MSELoss()

    # 整个训练过程只创建一次优化器
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=learning_rate,
    )

    # 训练前损失，以及之后每轮结束时的全数据损失
    full_loss_history = [
        evaluate_full_loss(model, X, y_true, criterion)
    ]

    # 每个epoch训练期间的按样本加权平均损失
    online_epoch_losses = []

    # 每个epoch实际处理的样本数量
    epoch_seen_counts = []

    for epoch in range(num_epochs):
        model.train()

        # 只统计当前epoch
        running_loss_sum = 0.0
        seen_count = 0
        seen_ids = []

        for batch_ids, batch_X, batch_y in train_loader:
            batch_size = batch_X.shape[0]

            seen_count += batch_size
            seen_ids.extend(batch_ids.tolist())

            # 清除上一个batch留下的梯度
            optimizer.zero_grad()

            # 当前batch前向传播
            batch_pred = model(batch_X)

            if batch_pred.shape != batch_y.shape:
                raise ValueError(
                    f"batch预测与标签shape不一致："
                    f"batch_pred={batch_pred.shape}, "
                    f"batch_y={batch_y.shape}"
                )

            # 当前batch的平均MSE
            batch_loss = criterion(batch_pred, batch_y)

            # 将batch平均损失还原成该batch的损失总和
            running_loss_sum += batch_loss.item() * batch_size

            # 计算当前batch对应的梯度
            batch_loss.backward()

            # 使用梯度更新模型参数
            optimizer.step()

        # 已退出batch循环，但仍处于当前epoch循环中

        if seen_count != X.shape[0]:
            raise RuntimeError(
                f"当前epoch处理样本数错误："
                f"seen_count={seen_count}, "
                f"expected={X.shape[0]}"
            )

        if sorted(seen_ids) != list(range(X.shape[0])):
            raise RuntimeError(
                f"当前epoch样本ID异常："
                f"seen_ids={seen_ids}"
            )

        # 当前epoch所有样本的在线平均损失
        online_epoch_loss = running_loss_sum / seen_count

        # 每个epoch各记录一次
        online_epoch_losses.append(online_epoch_loss)
        epoch_seen_counts.append(seen_count)

        # 使用本轮训练结束后的参数，对全部9个样本重新计算损失
        current_full_loss = evaluate_full_loss(
            model,
            X,
            y_true,
            criterion,
        )

        full_loss_history.append(current_full_loss)
        
    return (
        full_loss_history,
        online_epoch_losses,
        epoch_seen_counts,
    )
    
full_loss_history, online_epoch_losses, epoch_seen_counts = train_minibatch(
    model=model,
    train_loader=train_loader,
    X=X,
    y_true=y_true,
    learning_rate=0.05,
    num_epochs=50,
)

print("len(full_loss_history) =", len(full_loss_history))
print("len(online_epoch_losses) =", len(online_epoch_losses))
print("len(epoch_seen_counts) =", len(epoch_seen_counts))

print("initial full loss =", full_loss_history[0])
print("first online epoch loss =", online_epoch_losses[0])
print("first epoch full loss =", full_loss_history[1])
print("final full loss =", full_loss_history[-1])

print("epoch seen counts =", epoch_seen_counts)

print(
    "final weight =",
    model.linear.weight.detach().numpy(),
)
print(
    "final bias =",
    model.linear.bias.detach().numpy(),
)

drop_loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=False,
    drop_last=True,
    num_workers=0,
)

drop_seen_ids = []

for batch_ids, batch_X, batch_y in drop_loader:
    drop_seen_ids.extend(batch_ids.tolist())

missing_ids = sorted(
    set(sample_ids.tolist()) - set(drop_seen_ids)
)

print("drop len(loader) =", len(drop_loader))
print("drop seen count =", len(drop_seen_ids))
print("drop seen ids =", drop_seen_ids)
print("drop missing ids =", missing_ids)

generator = torch.Generator().manual_seed(42)

shuffle_loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True,
    drop_last=False,
    num_workers=0,
    generator=generator,
)

shuffle_seen_ids = []

for batch_ids, batch_X, batch_y in shuffle_loader:
    shuffle_seen_ids.extend(batch_ids.tolist())

print("shuffle seen ids =", shuffle_seen_ids)
print("shuffle sorted ids =", sorted(shuffle_seen_ids))
print("shuffle seen count =", len(shuffle_seen_ids))

is_monotonic = all(
    full_loss_history[index + 1]
    <= full_loss_history[index] + 1e-12
    for index in range(len(full_loss_history) - 1)
)

print("full loss monotonic =", is_monotonic)