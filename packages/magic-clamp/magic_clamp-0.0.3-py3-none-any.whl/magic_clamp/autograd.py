from typing import Optional

import torch


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
