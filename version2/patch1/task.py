"""Task - This class represents a task with a name, subject, priority, and a boolean
for whether or not the task has been competed."""

from version2.patch1.date import Date
from datetime import datetime


class Task:
    """This class stores information about a task."""

    def __init__(self, name="", subject="", priority=1, due_date_string="None", is_completed=False):
        """Initialize Task class, setting name, subject, priority and is_completed."""
        self.name = name
        self.subject = subject
        self.priority = priority
        self.due_date = Date(due_date_string)
        self.is_completed = is_completed

    def __str__(self):
        """Define rules for printing class objects."""
        return "{} in {}, priority {}{}{}".format(
            self.name, self.subject, self.priority,
            ", due {}".format(self.due_date) if self.due_date.is_valid_date() else "",
            " (completed)" if self.is_completed else "")

    def mark_as_completed(self):
        """Mark the task as completed."""
        self.is_completed = True

    def mark_as_uncompleted(self):
        """Mark the task as uncompleted."""
        self.is_completed = False

    def is_important(self):
        """Return True if task is important, False if it is not."""
        return self.priority <= 3

    def is_due(self):
        """Return True if task is due today or overdue, False if it is not."""
        current_date_string = "{}/{}/{}".format(datetime.now().day, datetime.now().month, datetime.now().year)
        current_date = Date("{}/{}/{}".format(
            datetime.now().day,
            datetime.now().month,
            datetime.now().year
        ))
        if self.due_date.is_valid_date():
            return not current_date < self.due_date
        else:
            return False


if __name__ == '__main__':
    task1 = Task("assignment", "cp1401", 1, "13/10/2020")
    task2 = Task("lecture", "cp1404", 2, "14/10/2020")
    task3 = Task("prac", "cp1402", 3, "None")
    print(task1)
    print(task2)
    print(task3)
    print(task1.due_date < task2.due_date)
    print(task1.due_date.is_valid_date())
    print(task3.is_due())
    print(task3.due_date.is_leap_year())
    print(task3.due_date.is_valid_date())
