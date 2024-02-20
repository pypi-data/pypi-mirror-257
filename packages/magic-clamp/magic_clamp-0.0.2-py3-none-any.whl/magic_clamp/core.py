from typing import Optional

import torch
import torch.nn as nn

from .autograd import ClampWithConditionalSTEFunction


def magic_clamp(
    x: torch.Tensor, min_value: Optional[float], max_value: Optional[float]
) -> torch.Tensor:
    """
    Forward pass: Clamps the input tensor.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
        min_value: The minimum value to clamp the input tensor.
        max_value: The maximum value to clamp the input tensor.
    """
    return ClampWithConditionalSTEFunction.apply(x, min_value, max_value)


def magic_hardsigmoid(x: torch.Tensor) -> torch.Tensor:
    """
    Forward pass: Applies the hard sigmoid function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
    """
    x = ClampWithConditionalSTEFunction.apply(x, -3.0, 3.0)
    x = x + 3.0
    x = x / 6.0
    return x


def magic_hardtanh(x: torch.Tensor) -> torch.Tensor:
    """
    Forward pass: Applies the hard tanh function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
    """
    return torch.clamp(x, -1.0, 1.0)


def magic_relu(x: torch.Tensor) -> torch.Tensor:
    """
    Forward pass: Applies the ReLU function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.
    """
    return torch.clamp(x, 0.0, None)


class MagicClamp(nn.Module):
    """
    A module that clamps the input tensor, using the conditional STE for gradient flow
    in clipped regions.

    Args:
        min_value: The minimum value to clamp the input tensor.
        max_value: The maximum value to clamp the input tensor.
        use_conditional_ste: Whether to use the conditional STE for gradient flow in
            clipped regions. If False, this is equivalent to using `torch.clamp`.
    """
    def __init__(
        self,
        min_value: Optional[float],
        max_value: Optional[float],
        use_conditional_ste: bool = True,
    ):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

        self.clamp_fn = magic_clamp if use_conditional_ste else torch.clamp

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.clamp_fn(x, self.min_value, self.max_value)
