"""Task Collection - This class represents a collection of tasks.
Functionality: loading & saving tasks to file, adding tasks to list, returning info, sorting."""

from operator import attrgetter
from version2.patch0.task import Task


class TaskCollection:
    """Collection of tasks with capability to add, read & write, sort and view info of tasks."""

    def __init__(self):
        """Initialize class, create tasks list."""
        self.tasks = []

    def __str__(self):
        """Define rules for printing class objects."""
        class_string = "Collection of {} tasks:\n".format(len(self.tasks))
        for task in self.tasks:
            class_string += str(task) + "\n"
        return class_string

    def load_tasks(self, file_name):
        """Read tasks from a file and add to tasks list."""
        file_in = open(file_name, 'r')
        for line in file_in:
            try:
                parts = line.strip().split(",")
                parts[2] = int(parts[2])
                parts[4] = parts[4] == "True"
                self.tasks.append(Task(parts[0], parts[1], parts[2], parts[3], parts[4]))
            except IndexError:
                print("Index error occurred when adding tasks")
                continue
            except ValueError:
                print("Value error occurred when adding tasks")
                continue
        file_in.close()

    def save_tasks(self, file_name):
        """Write all tasks to a file."""
        file_out = open(file_name, 'w')
        for task in self.tasks:
            print("{},{},{},{},{}".format(task.name, task.subject, task.priority, task.due_date, task.is_completed), file=file_out)
        file_out.close()

    def add_task(self, task=Task()):
        """Add Task object to tasks list and return a string confirming that task was added."""
        self.tasks.append(task)
        return str(task) + " added."

    def remove_task(self, task=Task()):
        """Remove Task object from tasks list and return the task that was removed."""
        if task in self.tasks:
            self.tasks.remove(task)
            return str(task) + " removed."

    def get_num_of_uncompleted_tasks(self):
        """Return the number of uncompleted tasks in tasks."""
        return len([task for task in self.tasks if not task.is_completed])

    def sort_tasks(self, key1="is_completed", key2="due_date", is_reversed=False):
        """Sort tasks list by passed in key first, then by priority."""
        self.tasks.sort(key=attrgetter(key1, key2, "priority"), reverse=is_reversed)
