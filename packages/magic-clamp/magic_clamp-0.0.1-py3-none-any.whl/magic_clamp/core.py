from typing import Optional

import torch
import torch.nn as nn

from .autograd import ClampWithConditionalSTEFunction


def magic_clamp(
    x: torch.Tensor, min_value: Optional[float], max_value: Optional[float]
) -> torch.Tensor:
    return ClampWithConditionalSTEFunction.apply(x, min_value, max_value)


class MagicClamp(nn.Module):
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
