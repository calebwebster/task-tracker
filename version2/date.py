"""
This class represents a date object. This object contains a day, month, and year and has
various methods such as:
is_valid_date
is_leap_year
__lt__ for sorting
"""


class Date:
    """Date object."""

    def __init__(self, parts):
        """Initialize Date object."""
        self.parts = parts
        if self.parts != "None":
            self.day = int(parts[0])
            self.month = int(parts[1])
            self.year = int(parts[2])

    def __str__(self):
        """Define rules for printing class objects."""
        if self.parts != "None":
            return "{}/{}/{}".format(self.day, self.month, self.year)
        else:
            return "None"

    def __lt__(self, other):
        """Return True if date object is less than other, False if it is not."""
        if self.parts != "None" and other.parts != "None":
            return self.year < other.year or self.month < other.month or self.day < other.day
        elif self.parts != "None" and other.parts == "None":
            return False
        elif self.parts == "None" and other.parts != "None":
            return True

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
        if self.parts != "None":
            return self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0
        else:
            return False
