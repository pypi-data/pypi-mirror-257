from os import getenv

PROFILING = int(getenv("PROFILING", "0"))

if not PROFILING:
    import matplotlib.pyplot as plt
    import numpy as np

###############################################################################

from random import random

from cudagrad.nn import Module, mse, sgd
from cudagrad.tensor import Tensor


class Linear(Module):
    def __init__(self, inputs: int, outputs: int):
        self.w = Tensor([outputs, inputs], [random() for _ in range(outputs * inputs)])
        self.b = Tensor([outputs], [random() for _ in range(outputs)])

    def __call__(self, x: Tensor) -> Tensor:
        return (self.w @ x) + self.b


if __name__ == "__main__":
    # OR
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = [0, 1, 1, 1]

    EPOCHS = 1000
    lr = 0.0001
    epochs = []
    losses = []
    model = Linear(2, 1)
    for epoch in range(EPOCHS + 1):
        for i, input in enumerate(inputs):
            model.zero_grad()
            loss = mse(Tensor([1], [targets[i]]), model(Tensor([2, 1], input)))
            loss.backward()
            sgd(model, lr)
        if epoch % (EPOCHS // 10) == 0:
            print(f"{epoch=}", f"{loss.item()}")
            epochs.append(epoch)
            losses.append(loss.item())
            out0 = round(model(Tensor([2, 1], inputs[0])).item())
            out1 = round(model(Tensor([2, 1], inputs[1])).item())
            out2 = round(model(Tensor([2, 1], inputs[2])).item())
            out3 = round(model(Tensor([2, 1], inputs[3])).item())
            print(
                "0 OR 0 = ",
                round(model(Tensor([2, 1], inputs[0])).item(), 2),
                "🔥" if out0 == 0 else "",
            )
            print(
                "0 OR 1 = ",
                round(model(Tensor([2, 1], inputs[1])).item(), 2),
                "🔥" if out1 == 1 else "",
            )
            print(
                "1 OR 0 = ",
                round(model(Tensor([2, 1], inputs[2])).item(), 2),
                "🔥" if out2 == 1 else "",
            )
            print(
                "1 OR 1 = ",
                round(model(Tensor([2, 1], inputs[3])).item(), 2),
                "🔥" if out3 == 1 else "",
            )

    if not PROFILING:
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros(X.shape)

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = model(Tensor([2, 1], [X[i, j], Y[i, j]])).item()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')

        plt.title('OR Neuron')
        plt.xlabel('X')
        plt.ylabel('Y')
        ax.set_zlabel('Z')
        plt.savefig("./cudagrad/plots/linear-3d.jpg")
