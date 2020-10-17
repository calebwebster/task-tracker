"""
Task Tracker version 2.1
15/10/2020
Kivy app that displays a list of tasks in GUI form.
User can add new tasks, change task sorting, and mark tasks as completed/uncompleted.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from version2.patch1.task import Task
from version2.patch1.taskcollection import TaskCollection
from version2.patch1.date import Date
import pygame

pygame.init()

SPINNER_SELECTIONS_TO_ATTRIBUTES = {"Priority": "priority", "Subject": "subject",
                                    "Name": "name", "Due Date": "due_date"}
STARTING_SPINNER_SELECTION_INDEX = 0
TASKS_FILE_NAME = "tasks.csv"
COMPLETED_COLOR = (.4, .4, .4, 1)  # 102,102,102
UNCOMPLETED_COLOR = (.2, .4, .6, 1)  # 51,102,153
RED = (1, 0, 0, 1)  # 255,0,0
WHITE = (1, 1, 1, 1)  # 255,255,255
MARONE = (.6, .2, .4, 1)  # 153,51,102
TEAL = (0, .6, .6, 1)  # 0,153,153
COMPLETED_SOUND = "trumpet.wav"


class PrioritySpinner(Spinner, Button):
    pass


class TaskLabel(Label):
    pass


class BoxLayout(BoxLayout, Button):
    pass


class SortingSpinnerOption(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = MARONE
        self.size_hint_y = None
        self.height = "48dp"


class PrioritySpinnerOption(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = TEAL
        self.size_hint_y = None
        self.height = "48dp"


class TaskTrackerApp(App):
    """App that interacts with GUI and utilises Task and TaskCollection classes."""

    tasks_to_complete_text = StringProperty()
    info_panel_text = StringProperty()
    number_of_buttons = NumericProperty()
    tasks_box_height = NumericProperty()
    spinner_selections = ListProperty()
    sorting_spinner_options = ObjectProperty(SortingSpinnerOption)
    priority_spinner_options = ObjectProperty(PrioritySpinnerOption)

    def __init__(self, **kwargs):
        """Initialize TravelTrackerApp class, load tasks into task_collection from tasks.csv."""
        super().__init__(**kwargs)
        self.task_collection = TaskCollection()
        self.task_collection.load_tasks(TASKS_FILE_NAME)
        self.spinner_selections = sorted(SPINNER_SELECTIONS_TO_ATTRIBUTES.keys())
        self.buttons = []
        self.priority_spinners = []
        self.sorting_is_reversed = False
        self.grouping_completed_tasks = True

    def build(self):
        """Construct the GUI, setting string and list properties to starting values."""
        self.title = "TaskTracker 2.0"
        self.icon = "icon.png"
        Window.size = (900, 600)
        self.root = Builder.load_file("app.kv")
        self.info_panel_text = "Welcome to TaskTracker 2.0"
        self.refresh_buttons()
        return self.root

    def on_stop(self):
        """Save tasks to tasks.csv when program ends."""
        self.task_collection.save_tasks(TASKS_FILE_NAME)

    def mark_completed_or_uncompleted(self, instance):
        """If task is completed, mark it as uncompleted. If task is uncompleted, mark it as
        completed. Refresh buttons, update tasks_to_complete and display info message according to
        task state and importance."""
        # Access button's task object
        task = instance.task
        if task.is_completed:
            task.mark_as_uncompleted()
            message = "You need to complete {}.".format(task.name)
            message += " Get to work!" if task.is_important() else ""
        else:
            task.mark_as_completed()
            self.play_sound(COMPLETED_SOUND)
            message = "You completed {}.".format(task.name)
            message += " Great work!" if task.is_important() else ""

        self.info_panel_text = message
        self.refresh_buttons()

    def refresh_buttons(self):
        """Remove all buttons, sort tasks, then create task buttons with task text,
        function binding, and background colours depending on whether task has been
        completed or not."""
        self.root.ids.tasks_box.clear_widgets()
        self.number_of_buttons = 0
        # Get sorting attributes
        attribute2 = SPINNER_SELECTIONS_TO_ATTRIBUTES[self.root.ids.sorting_attribute_selection.text]
        attribute1 = "is_completed" if self.grouping_completed_tasks else attribute2
        self.task_collection.sort_tasks(key1=attribute1, key2=attribute2, is_reversed=self.sorting_is_reversed)

        for button_number, task in enumerate(self.task_collection.tasks, 1):
            task_button = BoxLayout(
                id="button_{}".format(button_number),
                background_color=COMPLETED_COLOR if task.is_completed else UNCOMPLETED_COLOR,
                on_release=self.mark_completed_or_uncompleted
            )
            name_label = TaskLabel(text=task.name)
            subject_label = TaskLabel(text=task.subject, size_hint_x=0.8)
            due_date_label = TaskLabel(
                text=str(task.due_date),
                size_hint_x=0.6,
                color=RED if task.is_due() and not task.is_completed else WHITE,
            )
            priority_spinner = PrioritySpinner(
                id="button_{}_priority".format(button_number),
                text=str(task.priority),
                background_color = COMPLETED_COLOR if task.is_completed else UNCOMPLETED_COLOR,
            )
            # store reference to button's task object
            task_button.task = task
            priority_spinner.task = task

            task_button.add_widget(name_label)
            task_button.add_widget(subject_label)
            task_button.add_widget(due_date_label)

            self.root.ids.tasks_box.add_widget(task_button)
            self.root.ids.tasks_box.add_widget(priority_spinner)
            self.buttons.append(task_button)
            self.priority_spinners.append(priority_spinner)
        self.number_of_buttons = len(self.task_collection.tasks)
        self.tasks_box_height = self.number_of_buttons * 50

        num_of_uncompleted_tasks = self.task_collection.get_num_of_uncompleted_tasks()
        self.tasks_to_complete_text = "Tasks to complete: {}".format(num_of_uncompleted_tasks)

    def add_task(self):
        """Get task name, subject, and priority, and if they are valid,
        add Task to task_collection and refresh buttons."""
        name = self.root.ids.name_input.text.title()
        subject = self.root.ids.subject_input.text.title()
        priority = self.root.ids.priority_input.text
        due_date_string = self.root.ids.due_date_input.text.title()

        if name and subject and priority:
            try:
                priority = int(priority)
                # Due date entered can be a date (dd/mm/yyyy), "None", or ""
                if due_date_string != "":
                    temp_date_object = Date(due_date_string)
                else:
                    due_date_string = "None"
                if priority <= 0:
                    self.info_panel_text = "Priority must be > 0"
                else:
                    # task_collection.add_task() returns a confirmation message:
                    confirmation = self.task_collection.add_task(Task(
                        name, subject, priority, due_date_string
                    ))
                    self.info_panel_text = confirmation

                    # Utilize variable arguments to clear text of any amount of widgets
                    self.clear_widget_text(
                        self.root.ids.name_input, self.root.ids.subject_input,
                        self.root.ids.priority_input, self.root.ids.due_date_input
                    )
                    self.refresh_buttons()
            except ValueError:
                if isinstance(priority, int):
                    self.info_panel_text = "Please enter a valid date (dd/mm/yyyy) or leave blank"
                else:
                    self.info_panel_text = "Please enter a valid priority"
        else:
            self.info_panel_text = "All fields must be completed"

    def remove_completed_tasks(self):
        """Remove completed task buttons."""
        if self.task_collection.get_num_of_uncompleted_tasks() < len(self.task_collection.tasks):
            self.info_panel_text = "All completed tasks removed."
        for button in self.buttons:
            if button.task.is_completed:
                self.task_collection.remove_task(button.task)
                self.root.ids.tasks_box.remove_widget(button)
                self.root.ids.tasks_box.remove_widget(self.priority_spinners[self.buttons.index(button)])

    def reverse_sorting(self):
        """Reverse the sorting of tasks."""
        self.sorting_is_reversed = not self.sorting_is_reversed
        self.refresh_buttons()

    def group_or_ungroup(self):
        """Toggle is_completed as the first sorting attribute."""
        self.grouping_completed_tasks = not self.grouping_completed_tasks
        self.refresh_buttons()

    def increment_priority(self, instance):
        """Increment task priority by an amount passed in."""
        amount = int(instance.text)
        if amount > 0 or instance.task.priority > 1:
            instance.task.priority += amount
        self.refresh_buttons()

    @staticmethod
    def clear_widget_text(*widgets):
        """Clear the text of any number of any number of widgets passed in."""
        for widget in widgets:
            widget.text = ""

    @staticmethod
    def play_sound(sound):
        """Play the sound of the file passed in using playsound module."""
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound))


if __name__ == '__main__':
    TaskTrackerApp().run()
