"""
This class represents a date object. This object contains a day, month, and year and has
various methods such as:
is_valid_date
is_leap_year
__lt__ for sorting
"""


class Date:
    """Date object."""

    def __init__(self, string):
        """Initialize Date object."""
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
        if not self.is_none and not other.is_none:
            if self.year < other.year:
                return True
            elif self.year > other.year:
                return False
            else:
                if self.month < other.month:
                    return True
                elif self.month > other.month:
                    return False
                else:
                    if self.day < other.day:
                        return True
                    else:
                        return False
        elif not self.is_none and other.is_none:
            return True
        elif self.is_none and not other.is_none:
            return False
        else:
            return False

    def is_valid_date(self):
        """Return True if date is valid, False if it is not."""
        months_dict = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                       7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        try:
            if self.year >= 0 and 0 < self.month <= 12 and 0 < self.day <= months_dict[self.month]:
                if not self.is_leap_year() and self.month == 2 and self.day == 29:
                    return False
                else:
                    return True
            else:
                return False
        except ValueError:
            return False
        except IndexError:
            return False
        except:
            return False

    def is_leap_year(self):
        """Return True if year is a leap year, False if it is not."""
        if not self.is_none:
            return self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0
        else:
            return False
