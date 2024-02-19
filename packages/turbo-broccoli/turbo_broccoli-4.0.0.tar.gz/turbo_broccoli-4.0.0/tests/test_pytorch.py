# pylint: disable=missing-function-docstring
"""Pytorch (de)serialization test suite"""

import torch
from common import to_from_json

from turbo_broccoli import Context


class _TestModule(torch.nn.Module):
    module: torch.nn.Module

    def __init__(self):
        super().__init__()
        self.module = torch.nn.Sequential(
            torch.nn.Linear(4, 2),
            torch.nn.ReLU(),
            torch.nn.Linear(2, 1),
            torch.nn.ReLU(),
        )

    def forward(self, x):
        return self.module.forward(x)


def test_pytorch_numerical():
    x = torch.Tensor()
    assert to_from_json(x).numel() == 0
    x = torch.Tensor([1, 2, 3])
    torch.testing.assert_close(x, to_from_json(x))
    x = torch.rand((10, 10))
    torch.testing.assert_close(x, to_from_json(x))


def test_pytorch_numerical_large():
    ctx = Context(min_artifact_size=0)
    x = torch.rand((100, 100), dtype=torch.float64)
    torch.testing.assert_close(x, to_from_json(x, ctx))


def test_pytorch_module():
    ctx = Context(pytorch_module_types=[_TestModule])
    x = torch.ones(4)
    a = _TestModule()
    b = to_from_json(a, ctx)
    torch.testing.assert_close(a(x), b(x))
