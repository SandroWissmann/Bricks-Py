from bricks.types.rgb_color import RGBColor

import pytest


class TestRGBColor:
    def test_init(self):
        obj = RGBColor(0x20, 0x10, 0x30, 0x40)
        assert obj.r == 0x20
        assert obj.g == 0x10
        assert obj.b == 0x30
        assert obj.a == 0x40

    @pytest.mark.parametrize(
        "r, g, b, a",
        [
            (0x00 - 1, 0x00, 0x00, 0x00),
            (0x00, 0x00 - 1, 0x00, 0x00),
            (0x00, 0x00, 0x00 - 1, 0x00),
            (0x00, 0x00, 0x00, 0x00 - 1),
            (0xFF + 1, 0x00, 0x00, 0x00),
            (0x00, 0xFF + 1, 0x00, 0x00),
            (0x00, 0x00, 0xFF + 1, 0x00),
            (0x00, 0x00, 0x00, 0xFF + 1),
        ],
    )
    def test_init_exception(self, r, g, b, a):
        with pytest.raises(ValueError):
            RGBColor(r, g, b, a)

