from bricks.game_objects.ball import Ball
from bricks.game_objects.platform import Platform
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point
from bricks.types.angle import Angle, Quadrant

from random import uniform
from numpy import deg2rad


def reflect(ball: Ball, obj: GameObject):
    if ball.angle.quadrant == Quadrant.I:
        if isinstance(obj, Platform):
            return _reflect_from_platform_quadrant_I(ball, obj)
        return _reflect_from_quadrant_I(ball, obj)
    if ball.angle.quadrant == Quadrant.II:
        if isinstance(obj, Platform):
            return _reflect_from_platform_quadrant_II(ball, obj)
        return _reflect_from_quadrant_II(ball, obj)
    if ball.angle.quadrant == Quadrant.III:
        return _reflect_from_quadrant_III(ball, obj)
    if ball.angle.quadrant == Quadrant.IV:
        return _reflect_from_quadrant_IV(ball, obj)
    return False


def _reflect_from_platform_quadrant_I(ball: Ball, platform: Platform) -> bool:
    if _intersects_with_bottom_y(ball, platform):
        return _reflect_horizontal_from_platform_quadrant_I(ball, platform)
    if _intersects_with_right_x(ball, platform):
        return _reflect_vertical_from_quadrant_I(ball, platform)
    return False


def _reflect_horizontal_from_platform_quadrant_I(
    ball: Ball, platform: Platform
) -> bool:
    if _is_inside_with_x(ball, platform):
        _reflect_horizontal_I_to_IV(ball, platform)
    elif _intersects_with_right_x(
        ball, platform
    ) and _not_through_with_right_x(ball, platform):
        _reflect_horizontal_I_to_IV(ball, platform)
    elif _intersects_with_left_x(ball, platform) and _not_through_with_left_x(
        ball, platform
    ):
        _reflect_horizontal_I_to_IV(ball, platform)
    else:
        return False
    _put_before_intersects_with_bottom_y(ball, platform)
    return True


def _reflect_horizontal_I_to_IV(ball: Ball, platform: Platform):
    x_right = platform.bottom_right.x
    x_left = platform.top_left.x
    x_center = x_right - (platform.width / 2.0)
    x_ball = ball.bottom_right.x

    factor = _calc_angle_factor(x_ball, x_left, x_center, x_right)
    new_quad_angle = deg2rad(60.0) - (deg2rad(45.0) - deg2rad(45.0) * factor)
    assert deg2rad(0.0) <= new_quad_angle <= deg2rad(90.0)

    ball.angle.mirror_horizontal
    ball.angle.quadrant_angle = new_quad_angle


def _reflect_from_platform_quadrant_II(ball: Ball, platform: Platform) -> bool:
    if _intersects_with_bottom_y(ball, platform):
        return _reflect_horizontal_from_platform_quadrant_II(ball, platform)
    if _intersects_with_left_x(ball, platform):
        return _reflect_vertical_from_quadrant_II(ball, platform)
    return False


def _reflect_horizontal_from_platform_quadrant_II(
    ball: Ball, platform: Platform
) -> bool:
    if _is_inside_with_x(ball, platform):
        _reflect_horizontal_II_to_III(ball, platform)
    elif _intersects_with_right_x(
        ball, platform
    ) and _not_through_with_right_x(ball, platform):
        _reflect_horizontal_II_to_III(ball, platform)
    elif _intersects_with_left_x(ball, platform) and _not_through_with_left_x(
        ball, platform
    ):
        _reflect_horizontal_II_to_III(ball, platform)
    else:
        return False
    _put_before_intersects_with_bottom_y(ball, platform)
    return True


def _reflect_horizontal_II_to_III(ball: Ball, platform: Platform):
    x_righ = platform.bottom_right.x
    x_left = platform.top_left.x
    x_center = x_left + (platform.width / 2.0)
    x_ball = ball.top_Left.x

    factor = _calc_angle_factor(x_ball, x_left, x_center, x_righ)
    new_quad_angle = deg2rad(30.0) + (deg2rad(45.0) - (deg2rad(45.0) * factor))
    assert deg2rad(0.0) <= new_quad_angle <= deg2rad(90.0)

    ball.angle.mirror_horizontal
    ball.angle.quadrant_angle = new_quad_angle


def _calc_angle_factor(
    x_ball: float, x_left: float, x_center: float, x_right: float
) -> float:
    assert x_left < x_center
    assert x_center < x_right

    x_ball = _clamp(x_left, x_ball, x_right)

    length = x_center - x_left
    if x_ball <= x_center:
        factor = (x_center - x_ball) / length
    else:
        factor = (x_ball - x_center) / length
    factor = _clamp(0.0, factor, 1.0)
    assert 0.0 <= factor <= 1.0
    return factor


def _reflect_from_quadrant_I(ball: Ball, obj: GameObject) -> bool:
    if _intersects_with_bottom_y(ball, obj):
        return _reflect_horizontal_from_quadrant_I(ball, obj)
    if _intersects_with_right_x(ball, obj):
        return _reflect_vertical_from_quadrant_(ball, obj)
    return False


def _reflect_horizontal_from_quadrant_I(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_x(ball, obj):
        _reflect_horizontal(ball)
    elif _intersects_with_right_x(ball, obj) and _not_through_with_right_x(
        ball, obj
    ):
        _reflect_horizontal_increased(ball)
    elif _intersects_with_left_x(ball, obj) and _not_through_with_left_x(
        ball, obj
    ):
        _reflect_horizontal_increased(ball)
    else:
        return False
    _put_before_intersects_with_bottom_y(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_vertical_from_quadrant_(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_y(ball, obj):
        _reflect_vertical(ball)
    elif _intersects_with_bottom_y(ball, obj) and _not_through_with_bottom_y(
        ball, obj
    ):
        _reflect_vertical_increased(ball)
    elif _intersects_with_top_y(ball, obj) and _not_through_with_top_y(
        ball, obj
    ):
        _reflect_vertical_increased(ball)
    else:
        return False
    _put_before_intersects_with_right_x(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_from_quadrant_II(ball: Ball, obj: GameObject) -> bool:
    if _intersects_with_bottom_y(ball, obj):
        return _reflect_horizontal_from_quadrant_II(ball, obj)
    if _intersects_with_left_x(ball, obj):
        return _reflect_vertical_from_quadrant_I(ball, obj)
    return False


def _reflect_horizontal_from_quadrant_II(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_x(ball, obj):
        _reflect_horizontal(ball)
    elif _intersects_with_right_x(ball, obj) and _not_through_with_right_x(
        ball, obj
    ):
        _reflect_horizontal_decreased(ball)
    elif _intersects_with_left_x(ball, obj) and _not_through_with_left_x(
        ball, obj
    ):
        _reflect_horizontal_decreased(ball)
    else:
        return False
    _put_before_intersects_with_bottom_y(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_vertical_from_quadrant_I(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_y(ball, obj):
        _reflect_vertical(ball)
    elif _intersects_with_bottom_y(ball, obj) and _not_through_with_bottom_y(
        ball, obj
    ):
        _reflect_vertical_decreased(ball)
    elif _intersects_with_top_y(ball, obj) and _not_through_with_top_y(
        ball, obj
    ):
        _reflect_vertical_decreased(ball)
    else:
        return False
    _put_before_intersects_with_left_x(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_from_quadrant_III(ball: Ball, obj: GameObject) -> bool:
    if _intersects_with_top_y(ball, obj):
        return _reflect_horizontal_from_quadrant_III(ball, obj)
    if _intersects_with_left_x(ball, obj):
        return _reflect_vertical_from_quadrant_II(ball, obj)
    return False


def _reflect_horizontal_from_quadrant_III(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_x(ball, obj):
        _reflect_horizontal(ball)
    elif _intersects_with_right_x(ball, obj) and _not_through_with_right_x(
        ball, obj
    ):
        _reflect_horizontal_increased(ball)
    elif _intersects_with_left_x(ball, obj) and _not_through_with_left_x(
        ball, obj
    ):
        _reflect_horizontal_increased(ball)
    else:
        return False
    _put_before_intersects_with_top_y(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_vertical_from_quadrant_II(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_y(ball, obj):
        _reflect_vertical(ball)
    elif _intersects_with_bottom_y(ball, obj) and _not_through_with_bottom_y(
        ball, obj
    ):
        _reflect_vertical_increased(ball)
    elif _intersects_with_top_y(ball, obj) and _not_through_with_top_y(
        ball, obj
    ):
        _reflect_vertical_increased(ball)
    else:
        return False
    _put_before_intersects_with_left_x(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_from_quadrant_IV(ball: Ball, obj: GameObject) -> bool:
    if _intersects_with_top_y(ball, obj):
        return _reflect_horizontal_from_quadrant_IV(ball, obj)
    if _intersects_with_right_x(ball, obj):
        return _reflect_vertical_from_quadrant_V(ball, obj)
    return False


def _reflect_horizontal_from_quadrant_IV(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_x(ball, obj):
        _reflect_horizontal(ball)
    elif _intersects_with_right_x(ball, obj) and _not_through_with_right_x(
        ball, obj
    ):
        _reflect_horizontal_decreased(ball)
    elif _intersects_with_left_x(ball, obj) and _not_through_with_left_x(
        ball, obj
    ):
        _reflect_horizontal_decreased(ball)
    else:
        return False
    _put_before_intersects_with_top_y(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _reflect_vertical_from_quadrant_V(ball: Ball, obj: GameObject) -> bool:
    if _is_inside_with_y(ball, obj):
        _reflect_vertical(ball)
    elif _intersects_with_bottom_y(ball, obj) and _not_through_with_bottom_y(
        ball, obj
    ):
        _reflect_vertical_decreased(ball)
    elif _intersects_with_top_y(ball, obj) and _not_through_with_top_y(
        ball, obj
    ):
        _reflect_vertical_decreased(ball)
    else:
        return False
    _put_before_intersects_with_right_x(ball, obj)
    ball.setAngle(_clamp_angle(ball.angle()))
    return True


def _clamp_angle(angle: Angle) -> Angle:
    """
    Certain angles in the game should be prohibited because they are not funny 
    to play. The Function checks if angle is in the forbidden area and adjusts 
    the angle.
    """
    delta_x = deg2rad(30.0)
    delta_y = deg2rad(15.0)

    new_angle = angle

    if _is_bigger(angle.value, deg2rad(0.0), delta_x):
        new_angle.value = deg2rad(0.0) + delta_x
    elif _is_smaller(angle.value, deg2rad(90.0), delta_y):
        new_angle.value = deg2rad(90.0) - delta_y
    elif _is_bigger(angle.value, deg2rad(90.0), delta_y):
        new_angle.value = deg2rad(90.0) + delta_y
    elif _is_smaller(angle.value, deg2rad(180.0), delta_x):
        new_angle.value = deg2rad(180.0) - delta_x
    elif _is_bigger(angle.value, deg2rad(180.0), delta_x):
        new_angle.value = deg2rad(180.0) + delta_x
    elif _is_smaller(angle.value, deg2rad(270.0), delta_y):
        new_angle.value = deg2rad(270.0) - delta_y
    elif _is_bigger(angle.value, deg2rad(270.0), delta_y):
        new_angle.value = deg2rad(270.0) + delta_y
    elif _is_smaller(angle.value, deg2rad(360.0), delta_x):
        new_angle.value = deg2rad(360.0) - delta_x

    return new_angle


def _is_smaller(angle: float, target_angle: float, delta: float) -> bool:
    return angle >= target_angle - delta and angle < target_angle


def _is_bigger(angle: float, target_angle: float, delta: float) -> bool:
    return angle >= target_angle and angle < target_angle + delta


def _intersects_with_right_x(obj_a: GameObject, obj_b: GameObject) -> bool:
    return (
        obj_a.bottom_right.x >= obj_b.top_left.x
        and obj_a.top_left.x < obj_b.top_left.x
    )


def _intersects_with_left_x(obj_a: GameObject, obj_b: GameObject) -> bool:
    return (
        obj_a.top_left.x <= obj_b.bottom_right.x
        and obj_a.bottom_right.x > obj_b.bottom_right.x
    )


def _intersects_with_top_y(obj_a: GameObject, obj_b: GameObject) -> bool:
    return (
        obj_a.top_left.y <= obj_b.bottom_right.y
        and obj_a.bottom_right.y > obj_b.bottom_right.y
    )


def _intersects_with_bottom_y(obj_a: GameObject, obj_b: GameObject) -> bool:
    return (
        obj_a.bottom_right.y >= obj_b.top_left.y
        and obj_a.top_left.y < obj_b.top_left.y
    )


def _is_inside_with_x(ball: Ball, game_obj: GameObject) -> bool:
    return (
        ball.top_left.x >= game_obj.top_left.x
        and ball.bottom_right.x <= game_obj.bottom_right.x
    )


def _is_inside_with_y(ball: Ball, game_obj: GameObject) -> bool:
    return (
        ball.top_left.y >= game_obj.top_left.y
        and ball.bottom_right.y <= game_obj.bottom_right.y
    )


def _not_through_with_right_x(obj_a: GameObject, obj_b: GameObject) -> bool:
    return obj_a.bottom_right.x <= obj_b.bottom_right.x


def _not_through_with_left_x(obj_a: GameObject, obj_b: GameObject) -> bool:
    return obj_a.top_left.x >= obj_b.top_left.x


def _not_through_with_top_y(obj_a: GameObject, obj_b: GameObject) -> bool:
    return obj_a.top_left.y >= obj_b.top_left.y


def _not_through_with_bottom_y(obj_a: GameObject, obj_b: GameObject) -> bool:
    return obj_a.bottom_right.y <= obj_b.bottom_right.y


def _reflect_horizontal(ball: Ball):
    ball.angle.mirror_horizontal()


def _reflect_horizontal_increased(ball: Ball):
    _reflect_horizontal(ball)
    ball.angle.quadrant_angle = _increase_quadrant_angle(
        ball.angle.quadrant_angle
    )


def _reflect_horizontal_decreased(ball: Ball):
    _reflect_horizontal(ball)
    ball.angle.quadrant_angle = _decrease_quadrant_angle(
        ball.angle.quadrant_angle
    )


def _reflect_vertical(ball: Ball):
    ball.angle.mirror_vertical()


def _reflect_vertical_increased(ball: Ball):
    _reflect_vertical(ball)
    ball.angle.quadrant_angle = _increase_quadrant_angle(
        ball.angle.quadrant_angle
    )


def _reflect_vertical_decreased(ball: Ball):
    _reflect_vertical(ball)
    ball.angle.quadrant_angle = _decrease_quadrant_angle(
        ball.angle.quadrant_angle
    )


def _put_before_intersects_with_right_x(obj_a: GameObject, obj_b: GameObject):
    obj_a.top_left.x = obj_b.top_left.x - obj_a.width


def _put_before_intersects_with_left_x(obj_a: GameObject, obj_b: GameObject):
    obj_a.top_left.x = obj_b.bottom_right.x


def _put_before_intersects_with_bottom_y(ball: Ball, obj: GameObject):
    ball.top_left.y = obj.top_left.y - ball.height


def _put_before_intersects_with_top_y(ball: Ball, obj: GameObject):
    ball.top_left.y = obj.bottom_right.y


def _increase_quadrant_angle(quadrant_angle: float) -> float:
    quadrant_angle *= _random(1.0, 1.5)
    return _clamp(0.0, quadrant_angle, deg2rad(60.0))


def _decrease_quadrant_angle(quadrant_angle: float) -> float:
    return quadrant_angle * _random(0.5, 1.0)


def _random(minimum: float, maximum: float) -> float:
    return uniform(minimum, maximum)


def _clamp(minimum, x, maximum) -> float:
    return max(minimum, min(x, maximum))
