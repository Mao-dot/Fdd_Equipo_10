from dataclasses import dataclass


@dataclass(frozen=True)
class Design:
    """Nominal geometry. Manufacturing offsets are documented separately."""

    width: float = 320.0
    depth: float = 310.0
    height: float = 380.0
    panel: float = 6.0
    aperture: float = 290.0
    sill: float = 18.0
    lintel: float = 283.0
    shelf: float = 322.0
    dish_diameter: float = 270.0
    dish_rim_height: float = 24.0
    carrier_diameter: float = 240.0
    carrier_thickness: float = 1.5
    scale_height: float = 30.7
    scale_reserve_height: float = 37.0
    scale_size: float = 120.0
    scale_clearance: float = 1.0
    optical_hole: float = 116.0
    optical_window: float = 130.0
    window_thickness: float = 2.0
    window_gasket: float = 1.0
    lens_z: float = 350.0
    lens_adjust: float = 4.0
    screen_z: float = 352.0
    screen_width: float = 56.3
    screen_height: float = 28.6
    door_gap: float = 1.5
    door_overlay: float = 5.0
    door_angle: float = 105.0
    laser_hole: float = 3.4
    printed_hole: float = 3.6
    vent_width: float = 78.0
    vent_slot: float = 5.0

    @property
    def center_y(self):
        return self.depth / 2

    @property
    def inside_x(self):
        return self.width / 2 - self.panel

    @property
    def inside_rear(self):
        return self.depth - self.panel

    @property
    def lid_z(self):
        return self.height - self.panel

    @property
    def window_z(self):
        return self.shelf + self.panel + self.window_gasket

    @property
    def carrier_z(self):
        return self.panel + self.scale_height

    @property
    def dish_z(self):
        return self.carrier_z + self.carrier_thickness

    @property
    def hinge_x(self):
        return -self.width / 2 + 3.5

    @property
    def hinge_y(self):
        return -self.door_gap - self.panel - 2.5

    @property
    def latch_x(self):
        return self.width / 2 - 9.5

    @property
    def door_outer_y(self):
        return -self.door_gap - self.panel

    def check(self):
        if self.aperture < self.dish_diameter + 20:
            raise ValueError("Passage must provide 20 mm diametral operating clearance")
        if (self.width - self.aperture) / 2 < 14:
            raise ValueError("Front jamb too narrow for hinge reinforcement")
        if self.depth - 2 * self.panel < self.dish_diameter + 20:
            raise ValueError("Insufficient chamber depth")
        if self.sill > self.dish_z or self.lintel > self.shelf - 15:
            raise ValueError("Vertical entrance or top fascia is infeasible")
        if self.scale_reserve_height < self.scale_height:
            raise ValueError("The reserved height cannot be smaller than the model")
