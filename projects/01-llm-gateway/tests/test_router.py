import pytest

from gateway.router import select_model


@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("What is S3?", "small"),
        ("Compare DynamoDB and Aurora step by step", "large"),
        ("x" * 1500, "large"),
    ],
)
def test_routing(prompt, expected):
    assert select_model(prompt, "small", "large") == expected
