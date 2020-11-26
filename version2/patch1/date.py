"""
This class represents a date object. This object contains a day, month, and year and has
various methods such as:
is_valid_date
is_leap_year
__lt__ for sorting
"""


class Date:
    """Date object which can either be "None" or a date with self.day, self.month, self.year.
    Date is passed in as a string."""

    def __init__(self, string):
        """Initialize Date object, setting day, month and year if string is not "None"."""
        self.string = string
        self.is_none = self.string == "None"
        if not self.is_none:
            self.day, self.month, self.year = [int(part) for part in self.string.split("/")]

    def __str__(self):
        """Define rules for printing class objects."""
        if not self.is_none:
            return "{}/{}/{}".format(self.day, self.month, self.year)
        else:
            return "None"

    def __lt__(self, other):
        """Return True if date object is less than other, False if it is not."""
        s_parts = [self.year, self.month, self.day]
        o_parts = [other.year, other.month, other.day]
        for x in range(len(s_parts)):
            if s_parts[x] != o_parts[x]:
                return s_parts[x] < o_parts[x]
        return False

    def is_valid_date(self):
        """Return True if date is valid, False if it is not."""
        months_dict = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                       7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        is_leap = lambda y: y % 4 == 0 and y % 100 != 0 or y % 400 == 0
        try:
            if self.year >= 0 and 0 < self.month <= 12 and 0 < self.day <= months_dict[self.month]:
                if not is_leap(self.year) and self.month == 2 and self.day == 29:
                    return False
                else:
                    return True
            else:
                return False
        except:
            return False
