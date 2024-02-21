from typing import Callable, Optional

import torch


class ConstraintWithHyperPGDFunction(torch.autograd.Function):
    """
    Applies an idempotent constraint in the forward pass, and uses it in the backward
    pass as a projection operator for hyper PGD.
    """

    @staticmethod
    def forward(
        ctx,
        x: torch.Tensor,
        constraint_fn: Callable,
        preserve_norm: bool,
        preserve_norm_dim: Optional[int] = None,
    ):
        """
        Args:
            x: The input tensor.
            constraint_fn: The constraint function to apply.
            preserve_norm: Whether to preserve the norm of the gradient after clipping.
                Empirically, helps with lateral movements along the constraint set
                boundary.
        """
        ctx.constraint_fn = constraint_fn
        ctx.preserve_norm = preserve_norm
        ctx.preserve_norm_dim = preserve_norm_dim

        y = constraint_fn(x)

        ctx.save_for_backward(x, y)

        return y

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        x, y = ctx.saved_tensors

        # Take a step in the ambient space
        step = y - grad_output

        # Project the step onto the constraint set
        step = ctx.constraint_fn(step)

        # Use difference as gradient
        grad = x - step

        if ctx.preserve_norm:
            in_norm = torch.norm(grad_output, keepdim=True, dim=ctx.preserve_norm_dim)
            out_norm = torch.norm(grad, keepdim=True, dim=ctx.preserve_norm_dim)

            grad = grad * (in_norm / out_norm.clamp(min=1e-12))

        return grad, None, None, None


class ClampWithConditionalSTEFunction(torch.autograd.Function):
    """Clamps in the forward pass and applies the conditional STE in the backward
    pass.
    """

    @staticmethod
    def forward(
        ctx,
        x: torch.Tensor,
        min_value: Optional[float],
        max_value: Optional[float],
        preserve_norm: bool,
    ):
        """
        Args:
            x: The input tensor.
            min_value: The minimum value to clamp the input tensor.
            max_value: The maximum value to clamp the input tensor.
            preserve_norm: Whether to preserve the norm of the gradient after clipping.
                Empirically, helps with lateral movements along the constraint set
                boundary.
        """
        mask = torch.zeros_like(x)

        if min_value is not None:
            mask = torch.where(x < min_value, -1.0, mask)

        if max_value is not None:
            mask = torch.where(x > max_value, 1.0, mask)

        ctx.save_for_backward(mask)
        ctx.preserve_norm = preserve_norm

        x = torch.clamp(x, min_value, max_value)

        return x

    @staticmethod
    def backward(ctx, grad_output):
        (mask,) = ctx.saved_tensors

        if ctx.preserve_norm:
            in_norm = torch.norm(grad_output)

        grad_output = torch.where((mask == 1.0) & (grad_output < 0), 0.0, grad_output)
        grad_output = torch.where((mask == -1.0) & (grad_output > 0), 0.0, grad_output)

        if ctx.preserve_norm:
            out_norm = torch.norm(grad_output)
            grad_output = grad_output * (in_norm / out_norm.clamp(min=1e-12))

        return grad_output, None, None, None
