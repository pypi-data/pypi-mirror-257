import torch


def project_to_sphere(x: torch.Tensor, radius: float = 1.0) -> torch.Tensor:
    """Projects the input tensor (..., K) onto the closure of a K-sphere.

    Args:
        x: The input tensor (..., K).
        radius: The radius of the sphere.

    Returns:
        The projected tensor.
    """

    norm = torch.norm(x, dim=-1, keepdim=True)
    clamped_norm = torch.clamp(norm, max=radius)

    return x * (clamped_norm / (norm.clamp(min=1e-12)))
