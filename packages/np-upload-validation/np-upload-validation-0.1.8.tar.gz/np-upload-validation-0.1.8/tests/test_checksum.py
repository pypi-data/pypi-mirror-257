import pytest
import logging
import dotenv
import numpy as np
import typing
from np_upload_validation import checksum


dotenv.load_dotenv()

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            (np.zeros((1000, 200)), 20, 1,),
            "5F75D10F",
        ),
        (
            (np.zeros((1000, 200)), 1000, 1,),
            "5F75D10F",
        ),
        (
            (np.ones((1000, 200)), 1000, 1,),
            "FAA28853",
        ),
    ]
)
def test_generate_checksum(args: tuple[typing.Any, ...], expected: str) -> None:
    assert checksum.checksum_array(*args) == expected


@pytest.mark.parametrize("args,expected", [
    (
        (
            np.array([
                np.arange(0, 384)
                for _ in range(10000)
            ]),
            10,
            1,
        ),
        np.arange(0, 384),
    ),
])
def test_array_slicer(args, expected) -> None:
    """Test that the way we traverse the array is the way we expect.
    """
    for slice in checksum._array_slicer(*args):
        assert (slice == expected).all()