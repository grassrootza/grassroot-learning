from rasa_core.slots import Slot

class GeoLocationSlot(Slot):

    def feature_dimensionality(self):
        return 2

    def as_feature(self):
        r = [0.0] * self.feature_dimensionality()
        if self.value:
            if self.value <= 6:
                r[0] = 1.0
            else:
                r[1] = 1.0
        return r
