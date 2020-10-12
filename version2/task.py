"""Task - This class represents a task with a name, subject, priority, and a boolean
for whether or not the task has been competed."""

import datetime


class Task:
    """This class stores information about a task."""

    def __init__(self, name="", subject="", priority=1, due_date="", is_completed=False):
        """Initialize Task class, setting name, subject, priority and is_completed."""
        self.name = name
        self.subject = subject
        self.priority = priority
        self.due_date = due_date
        self.is_completed = is_completed

    def __str__(self):
        """Define rules for printing class objects."""
        return "{} in {}, priority {}{}{}".format(
            self.name, self.subject, self.priority,
            ", due {}".format(self.due_date) if self.due_date else "",
            " (completed)" if self.is_completed else "")

    def mark_as_completed(self):
        """Mark the task as completed."""
        self.is_completed = True

    def mark_as_uncompleted(self):
        """Mark the task as uncompleted."""
        self.is_completed = False

    def is_important(self):
        """Return True if task is important, False if it is not."""
        return self.priority <= 2

    def is_due(self):
        """Return True if task is due today or overdue, False if it is not."""
        current_datetime = datetime.datetime.now()
        try:
            day, month, year = [int(part) for part in self.due_date.split("/")]
            due_datetime = datetime.datetime(year, month, day)
            return current_datetime >= due_datetime
        except ValueError:
            return False
        except IndexError:
            return False
