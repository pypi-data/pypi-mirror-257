from functools import partial
from typing import Callable, Optional

import torch
import torch.nn as nn

from magic_clamp.project import project_to_sphere

from .autograd import ClampWithConditionalSTEFunction, ConstraintWithHyperPGDFunction


def magic_clamp(
    x: torch.Tensor,
    min_value: Optional[float],
    max_value: Optional[float],
    preserve_norm: bool = True,
) -> torch.Tensor:
    """
    Forward pass: Clamps the input tensor.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
        min_value: The minimum value to clamp the input tensor.
        max_value: The maximum value to clamp the input tensor.
        preserve_norm: Whether to preserve the norm of the gradient after clipping.
            Empirically, helps with lateral movements along the constraint set boundary.
    """
    return ClampWithConditionalSTEFunction.apply(x, min_value, max_value, preserve_norm)


def magic_hardsigmoid(x: torch.Tensor, preserve_norm: bool = True) -> torch.Tensor:
    """
    Forward pass: Applies the hard sigmoid function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
    """
    x = magic_clamp(x, -3.0, 3.0, preserve_norm=preserve_norm)
    x = x + 3.0
    x = x / 6.0
    return x


def magic_hardtanh(x: torch.Tensor, preserve_norm: bool = True) -> torch.Tensor:
    """
    Forward pass: Applies the hard tanh function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.

    Args:
        x: The input tensor.
    """
    return magic_clamp(x, -1.0, 1.0, preserve_norm=preserve_norm)


def magic_relu(x: torch.Tensor, preserve_norm: bool = True) -> torch.Tensor:
    """
    Forward pass: Applies the ReLU function.
    Backward pass: Applies the conditional STE for gradient flow in clipped regions.
    """
    return magic_clamp(x, 0.0, None, preserve_norm=preserve_norm)


class MagicClamp(nn.Module):
    """
    A module that clamps the input tensor, using the conditional STE for gradient flow
    in clipped regions.

    Args:
        min_value: The minimum value to clamp the input tensor.
        max_value: The maximum value to clamp the input tensor.
        preserve_norm: Whether to preserve the norm of the gradient after clipping.
            Empirically, helps with lateral movements along the constraint set boundary.
        use_conditional_ste: Whether to use the conditional STE for gradient flow in
            clipped regions. If False, this is equivalent to using `torch.clamp`.
    """

    def __init__(
        self,
        min_value: Optional[float],
        max_value: Optional[float],
        preserve_norm: bool = True,
        use_conditional_ste: bool = True,
    ):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.preserve_norm = preserve_norm
        self.use_conditional_ste = use_conditional_ste

    def _get_clamp_fn(
        self,
    ) -> Callable:
        return (
            partial(
                magic_clamp,
                min_value=self.min_value,
                max_value=self.max_value,
                preserve_norm=self.preserve_norm,
            )
            if self.use_conditional_ste
            else partial(
                torch.clamp,
                min=self.min_value,
                max=self.max_value,
            )
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        clamp_fn = self._get_clamp_fn()
        return clamp_fn(x)


def magic_sphere(
    x: torch.Tensor,
    radius: float = 1.0,
    preserve_norm: bool = True,
    preserve_norm_dim: Optional[int] = -1,
) -> torch.Tensor:
    """Magic projection onto the closure of a K-sphere, using meta-PGD in the backward
    pass.

    Args:
        x: The input tensor (..., K).
        radius: The radius of the sphere.

    Returns:
        The projected tensor.
    """

    projection = partial(project_to_sphere, radius=radius)

    return ConstraintWithHyperPGDFunction.apply(
        x, projection, preserve_norm, preserve_norm_dim
    )
