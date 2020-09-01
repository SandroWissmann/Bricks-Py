from bricks.game_objects.ball import Ball
from bricks.game_objects.platform import Platform
from bricks.game_objects.brick import Brick
from bricks.game_objects.indestructible_brick import IndestructibleBrick
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point
from bricks.types.angle import Angle, Quadrant

from typing import List
from typing import Tuple
from enum import Enum

from random import uniform
from numpy import deg2rad


class _Intersection(Enum):
    NONE = (0,)
    LEFT = (1,)
    TOP_LEFT = (2,)
    TOP = (3,)
    TOP_RIGHT = (4,)
    RIGHT = (5,)
    BOTTOM_RIGHT = (6,)
    BOTTOM = (7,)
    BOTTOM_LEFT = 8


def reflect(ball: Ball, game_objects: List[GameObject]) -> bool:
    object_intersection_pairs = _get_object_intersection_pairs(
        ball, game_objects
    )
    if len(object_intersection_pairs) == 0:
        return False
    if len(object_intersection_pairs) == 1:
        _reflect_from_single_object(
            ball=ball,
            game_object=object_intersection_pairs[0][0],
            intersection=object_intersection_pairs[0][1],
        )
        return True
    if len(object_intersection_pairs) > 1:
        _reflect_from_multiple_objects(
            ball=ball, object_intersection_pairs=object_intersection_pairs
        )
        return True
    return False


def _get_object_intersection_pairs(
    ball: Ball, game_objects: List[GameObject]
) -> List[Tuple[GameObject, _Intersection]]:
    object_intersection_pairs = []
    for game_object in game_objects:
        intersection = _get_intersection(ball, game_object)
        if intersection != _Intersection.NONE:
            object_intersection_pairs.append((game_object, intersection))
    return object_intersection_pairs


def _get_intersection(ball: Ball, obj: GameObject) -> _Intersection:
    intersections: List[_Intersection] = []

    if _top_left_intersects_with_bottom_right(
        top_left_1=ball.top_left,
        bottom_right_2=obj.bottom_right,
        top_left_2=obj.top_left,
    ):
        intersections.append(_Intersection.BOTTOM_RIGHT)
    elif _top_right_intersects_with_bottom_left(
        top_right_1=ball.top_right,
        bottom_left_2=obj.bottom_left,
        top_right_2=obj.top_right,
    ):
        intersections.append(_Intersection.BOTTOM_LEFT)
    elif _bottom_left_intersects_with_top_right(
        bottom_left_1=ball.bottom_left,
        top_right_2=obj.top_right,
        bottom_left_2=obj.bottom_left,
    ):
        intersections.append(_Intersection.TOP_RIGHT)
    elif _bottom_right_intersects_with_top_left(
        bottom_right_1=ball.bottom_right,
        top_left_2=obj.top_left,
        bottom_right_2=obj.bottom_right,
    ):
        intersections.append(_Intersection.TOP_LEFT)

    if len(intersections) == 0:
        return _Intersection.NONE
    if len(intersections) == 1:
        return intersections[0]
    if len(intersections) == 2:
        if _interects_left(intersections):
            return _Intersection.LEFT
        if _interects_top(intersections):
            return _Intersection.TOP
        if _interects_right(intersections):
            return _Intersection.RIGHT
        if _interects_bottom(intersections):
            return _Intersection.BOTTOM
    return _Intersection.NONE


def _bottom_right_intersects_with_top_left(
    bottom_right_1: Point, top_left_2: Point, bottom_right_2: Point
) -> bool:
    """Bottom right of square 1 is inside the top left of square 2."""
    x_is_inside = top_left_2.x <= bottom_right_1.x < bottom_right_2.x
    y_is_inside = top_left_2.y <= bottom_right_1.y < bottom_right_2.y
    return x_is_inside and y_is_inside


def _bottom_left_intersects_with_top_right(
    bottom_left_1: Point, top_right_2: Point, bottom_left_2: Point
) -> bool:
    """Bottom left of square 1 is inside the top right of square 2."""
    x_is_inside = top_right_2.x >= bottom_left_1.x > bottom_left_2.x
    y_is_inside = top_right_2.y <= bottom_left_1.y < bottom_left_2.y
    return x_is_inside and y_is_inside


def _top_left_intersects_with_bottom_right(
    top_left_1: Point, bottom_right_2: Point, top_left_2: Point
) -> bool:
    """Top left of square 1 is inside the bottom right of square 2."""
    x_is_inside = bottom_right_2.x >= top_left_1.x > top_left_2.x
    y_is_inside = bottom_right_2.y >= top_left_1.y > top_left_2.y
    return x_is_inside and y_is_inside


def _top_right_intersects_with_bottom_left(
    top_right_1: Point, bottom_left_2: Point, top_right_2: Point
) -> bool:
    """Top right of square 1 is inside the bottom left of square 2."""
    x_is_inside = bottom_left_2.x <= top_right_1.x < top_right_2.x
    y_is_inside = bottom_left_2.y >= top_right_1.y > top_right_2.y
    return x_is_inside and y_is_inside


def _interects_left(intersections: List[_Intersection]) -> bool:
    return all(
        x in intersections
        for x in [_Intersection.BOTTOM_LEFT, _Intersection.TOP_LEFT]
    )


def _interects_top(intersections: List[_Intersection]) -> bool:
    return all(
        x in intersections
        for x in [_Intersection.TOP_LEFT, _Intersection.TOP_RIGHT]
    )


def _interects_right(intersections: List[_Intersection]) -> bool:
    return all(
        x in intersections
        for x in [_Intersection.TOP_RIGHT, _Intersection.BOTTOM_RIGHT]
    )


def _interects_bottom(intersections: List[_Intersection]) -> bool:
    return all(
        x in intersections
        for x in [_Intersection.BOTTOM_RIGHT, _Intersection.BOTTOM_LEFT]
    )


def _reflect_from_single_object(
    ball: Ball, game_object: GameObject, intersection: _Intersection
):
    if intersection == _Intersection.LEFT:
        _reflect_from_collision_with_left(ball, game_object)
    elif intersection == _Intersection.TOP_LEFT:
        if _intersection_is_more_left_than_top(ball, game_object):
            _reflect_from_collision_with_left(ball, game_object)
        else:
            _reflect_from_collision_with_top(ball, game_object)
    elif intersection == _Intersection.TOP:
        _reflect_from_collision_with_top(ball, game_object)
    elif intersection == _Intersection.TOP_RIGHT:
        if _intersection_is_more_top_than_right(ball, game_object):
            _reflect_from_collision_with_top(ball, game_object)
        else:
            _reflect_from_collision_with_right(ball, game_object)
    elif intersection == _Intersection.RIGHT:
        _reflect_from_collision_with_right(ball, game_object)
    elif intersection == _Intersection.BOTTOM_RIGHT:
        if _intersection_is_more_right_than_bottom(ball, game_object):
            _reflect_from_collision_with_right(ball, game_object)
        else:
            _reflect_from_collision_with_bottom(ball, game_object)
    elif intersection == _Intersection.BOTTOM:
        _reflect_from_collision_with_bottom(ball, game_object)
    elif intersection == _Intersection.BOTTOM_LEFT:
        if _intersection_is_more_bottom_than_left(ball, game_object):
            _reflect_from_collision_with_bottom(ball, game_object)
        else:
            _reflect_from_collision_with_left(ball, game_object)


def _reflect_from_multiple_objects(
    ball: Ball,
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]],
):
    assert len(object_intersection_pairs) > 1
    if _intersects_from_left_with_multi_objects(object_intersection_pairs):
        _reflect_from_collision_with_left(
            ball, object_intersection_pairs[0][0]
        )
    elif _intersects_from_top_with_multi_objects(object_intersection_pairs):
        _reflect_from_collision_with_top(ball, object_intersection_pairs[0][0])
    elif _intersects_from_right_with_multi_objects(object_intersection_pairs):
        _reflect_from_collision_with_right(
            ball, object_intersection_pairs[0][0]
        )
    elif _intersects_from_bottom_with_multi_objects(object_intersection_pairs):
        _reflect_from_collision_with_bottom(
            ball, object_intersection_pairs[0][0]
        )


def _intersects_from_left_with_multi_objects(
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]]
) -> bool:
    assert len(object_intersection_pairs) > 1

    valid_values = [
        _Intersection.LEFT,
        _Intersection.TOP_LEFT,
        _Intersection.BOTTOM_LEFT,
    ]
    return _object_intersection_pairs_contain_only_values_from_intersection_list(
        valid_values, object_intersection_pairs
    )


def _intersects_from_top_with_multi_objects(
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]]
) -> bool:
    assert len(object_intersection_pairs) > 1

    valid_values = [
        _Intersection.TOP,
        _Intersection.TOP_LEFT,
        _Intersection.TOP_RIGHT,
    ]
    return _object_intersection_pairs_contain_only_values_from_intersection_list(
        valid_values, object_intersection_pairs
    )


def _intersects_from_right_with_multi_objects(
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]]
) -> bool:
    assert len(object_intersection_pairs) > 1

    valid_values = [
        _Intersection.RIGHT,
        _Intersection.TOP_RIGHT,
        _Intersection.BOTTOM_RIGHT,
    ]
    return _object_intersection_pairs_contain_only_values_from_intersection_list(
        valid_values, object_intersection_pairs
    )


def _intersects_from_bottom_with_multi_objects(
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]]
) -> bool:
    assert len(object_intersection_pairs) > 1

    valid_values = [
        _Intersection.BOTTOM,
        _Intersection.BOTTOM_RIGHT,
        _Intersection.BOTTOM_LEFT,
    ]

    for object_intersection_pair in object_intersection_pairs:
        intersection = object_intersection_pair[1]
        if not intersection in valid_values:
            return False
    return True


def _object_intersection_pairs_contain_only_values_from_intersection_list(
    intersection_list: List[_Intersection],
    object_intersection_pairs=List[Tuple[GameObject, _Intersection]],
) -> bool:
    for object_intersection_pair in object_intersection_pairs:
        intersection = object_intersection_pair[1]
        if not intersection in intersection_list:
            return False
    return True


def _reflect_from_collision_with_left(ball: Ball, game_object: GameObject):
    _reflect_vertical(ball)
    _put_before_intersects_with_right_x(ball, game_object)


def _reflect_from_collision_with_top(ball: Ball, game_object: GameObject):
    _reflect_horizontal(ball)
    _put_before_intersects_with_bottom_y(ball, game_object)


def _reflect_from_collision_with_right(ball: Ball, game_object: GameObject):
    _reflect_vertical(ball)
    _put_before_intersects_with_left_x(ball, game_object)


def _reflect_from_collision_with_bottom(ball: Ball, game_object: GameObject):
    _reflect_horizontal(ball)
    _put_before_intersects_with_top_y(ball, game_object)


def _intersection_is_more_left_than_top(
    ball: Ball, game_object: GameObject
) -> bool:
    x = ball.bottom_right.x - game_object.top_left.x
    y = ball.bottom_right.y - game_object.top_left.y
    assert x >= 0
    assert y >= 0
    return y > x


def _intersection_is_more_top_than_right(
    ball: Ball, game_object: GameObject
) -> bool:
    x = game_object.top_right.x - ball.bottom_left.x
    y = ball.bottom_left.y - game_object.top_right.y
    assert x >= 0
    assert y >= 0
    return x > y


def _intersection_is_more_right_than_bottom(
    ball: Ball, game_object: GameObject
) -> bool:
    x = game_object.bottom_right.x - ball.top_left.x
    y = game_object.bottom_right.y - ball.top_left.y
    assert x >= 0
    assert y >= 0
    return y > x


def _intersection_is_more_bottom_than_left(
    ball: Ball, game_object: GameObject
) -> bool:
    x = ball.top_right.x - game_object.bottom_left.x
    y = game_object.bottom_left.y - ball.top_right.y
    assert x >= 0
    assert y >= 0
    return x > y


def _reflect_horizontal(ball: Ball):
    ball.angle.mirror_horizontal()


def _reflect_vertical(ball: Ball):
    ball.angle.mirror_vertical()


def _put_before_intersects_with_right_x(obj_a: GameObject, obj_b: GameObject):
    obj_a.top_left.x = obj_b.top_left.x - obj_a.width


def _put_before_intersects_with_left_x(obj_a: GameObject, obj_b: GameObject):
    obj_a.top_left.x = obj_b.bottom_right.x


def _put_before_intersects_with_bottom_y(ball: Ball, obj: GameObject):
    ball.top_left.y = obj.top_left.y - ball.height


def _put_before_intersects_with_top_y(ball: Ball, obj: GameObject):
    ball.top_left.y = obj.bottom_right.y


def _random(minimum: float, maximum: float) -> float:
    return uniform(minimum, maximum)


def _clamp(minimum, x, maximum) -> float:
    return max(minimum, min(x, maximum))
