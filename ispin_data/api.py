import numpy as np

class Data:
    """Get iSpin data for a specified turbine ID"""

    def __init__(self, case_sensitive=False):

        """Creates a detector parsing given data file"""
        self.case_sensitive = case_sensitive

    def _circle_area(self, ID):
        """Finds the area of a circle fiven by the specified turbine ID"""
        a = round(np.pi * ID**2)
        return a

    def request_data(self, ID):
        """Returns iSpin data for a specified turbine ID"""

        if type(ID) == int:
            return self._circle_area(self, ID)
        else:
            raise Exception("The provided turbine ID does not exists")
