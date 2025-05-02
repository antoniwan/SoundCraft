import util.math_helpers
from script.constants import ControlChangeType


class Deadzone:
    def __init__(self, maximum=1.0, centre=None, width=0.1):
        self.absolute_deadzone = AbsoluteDeadzone(maximum=maximum, centre=centre, width=width)
        self.relative_deadzone = RelativeDeadzone(maximum=maximum, centre=centre, width=width)

    def __call__(self, control_change_type: ControlChangeType, value, current_value):
        if control_change_type == ControlChangeType.Absolute:
            return self.absolute_deadzone(value)
        return self.relative_deadzone(delta=value, current_value=current_value)


class RelativeDeadzone:
    def __init__(self, maximum, centre, width):
        self.maximum = maximum
        self.centre = centre
        self.width = width
        self.distance_left = 0

    @property
    def _distance_left_is_zero(self):
        return abs(self.distance_left) < 1e-3

    def __call__(self, delta, current_value):
        if self.centre is None:
            return util.math_helpers.clamp(current_value + delta, 0, self.maximum)

        if abs(current_value - self.centre) > 1e-3:
            self.distance_left = 0

        if self._distance_left_is_zero:
            new_value = current_value + delta
            crosses_threshold = (current_value < self.centre < new_value) or (current_value > self.centre > new_value)
            if crosses_threshold:
                delta = delta - (self.centre - current_value)
                self.distance_left = self.width

        distance_left_is_smaller_than_delta = self.distance_left < abs(delta)

        if not distance_left_is_smaller_than_delta:
            self.distance_left = self.distance_left - abs(delta)
        elif not self._distance_left_is_zero and distance_left_is_smaller_than_delta:
            delta = delta - self.distance_left
            self.distance_left = 0

        if abs(self.distance_left) > 1e-3:
            return self.centre

        return util.math_helpers.clamp(current_value + delta, 0, self.maximum)


class AbsoluteDeadzone:
    def __init__(self, maximum, centre, width):
        self.deadzone_centre = centre
        if centre is not None:
            self.deadzone_lower = centre - width / 2
            self.deadzone_upper = centre + width / 2
            self.upper_scalar = (maximum - self.deadzone_centre) / (maximum - self.deadzone_upper)
            self.lower_scalar = self.deadzone_centre / self.deadzone_lower

    def __call__(self, value):
        if self.deadzone_centre is None:
            return value

        if value >= self.deadzone_upper:
            return (value - self.deadzone_upper) * self.upper_scalar + self.deadzone_centre

        if value > self.deadzone_lower:
            return self.deadzone_centre

        return value * self.lower_scalar
