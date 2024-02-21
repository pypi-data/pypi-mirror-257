import torch

from condste.autograd import ClampWithConditionalSTEFunction

def test_clamp_with_conditional_ste():
    input = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    target = torch.tensor([9.0, 9.0, 9.0])
    min_value = 1.5
    max_value = 2.5

    output = ClampWithConditionalSTEFunction.apply(input, min_value, max_value)

    loss = torch.nn.functional.l1_loss(output, target, reduction="sum")
    loss.backward()

    assert torch.allclose(output, torch.tensor([1.5, 2.0, 2.5]))
    assert torch.allclose(input.grad, torch.tensor([-1.0, -1.0, 0.0]))
