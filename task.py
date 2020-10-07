"""Task - This class represents a task with a name, subject, priority, and a boolean
for whether or not the task has been competed."""


class Task:
    """This class stores information about a task."""

    def __init__(self, name="", subject="", priority=0, is_completed=False):
        """Initialize Task class, setting name, subject, priority and is_completed."""
        self.name = name
        self.subject = subject
        self.priority = priority
        self.is_completed = is_completed

    def __str__(self):
        """Define rules for printing class objects."""
        return "{} in {}, priority {}{}".format(self.name, self.subject, self.priority,
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
