class PhysicsService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self):
        if self._is_initialized:
            return
        self._g = 9.81
        self._calculation_count = 0
        self._is_initialized = True

    def set_gravity(self, gravity_value):
        self._g = gravity_value

    def get_gravity(self):
        return self._g

    def weight_force(self, mass):
        self._calculation_count += 1
        return mass * self._g

    def free_fall_distance(self, time_seconds):
        self._calculation_count += 1
        return 0.5 * self._g * (time_seconds ** 2)

    def get_calculation_count(self):
        return self._calculation_count