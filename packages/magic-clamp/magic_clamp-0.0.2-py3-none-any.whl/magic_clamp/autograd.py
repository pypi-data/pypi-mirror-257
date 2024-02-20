from typing import Optional

import torch


class ClampWithConditionalSTEFunction(torch.autograd.Function):
    """Clamps in the forward pass and applies the conditional STE in the backward 
    pass.
    """
    @staticmethod
    def forward(
        ctx, x: torch.Tensor, min_value: Optional[float], max_value: Optional[float]
    ):
        """
        Args:
            x: The input tensor.
            min_value: The minimum value to clamp the input tensor.
            max_value: The maximum value to clamp the input tensor.
        """
        mask = torch.zeros_like(x)

        if min_value is not None:
            mask = torch.where(x < min_value, -1.0, mask)

        if max_value is not None:
            mask = torch.where(x > max_value, 1.0, mask)

        ctx.save_for_backward(mask)

        x = torch.clamp(x, min_value, max_value)

        return x

    @staticmethod
    def backward(ctx, grad_output):
        (mask,) = ctx.saved_tensors

        grad_output = torch.where((mask == 1.0) & (grad_output < 0), 0.0, grad_output)
        grad_output = torch.where((mask == -1.0) & (grad_output > 0), 0.0, grad_output)

        return grad_output, None, None
