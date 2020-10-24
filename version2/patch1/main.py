"""
Task Tracker version 2.1
22/10/2020
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
from kivy.uix.popup import Popup
from version2.patch1.task import Task
from version2.patch1.taskcollection import TaskCollection
from version2.patch1.date import Date
import pygame

pygame.init()

SETTINGS_FILE = "settings.txt"
HELP_FILE = "help.txt"
SPINNER_SELECTIONS_TO_ATTRIBUTES = {"Priority": "priority", "Subject": "subject",
                                    "Name": "name", "Due Date": "due_date"}
STARTING_SPINNER_SELECTION_INDEX = 0


class PrioritySpinner(Spinner, Button):
    pass


class TaskLabel(Label):
    pass


class ButtonBoxLayout(BoxLayout, Button):
    pass


class HelpPopup(Popup):
    pass


class SortingSpinnerOption(Button):
    pass


class PrioritySpinnerOption(Button):
    pass


class TaskTrackerApp(App):
    """App that interacts with GUI and utilises Task and TaskCollection classes."""

    completed_color = ()
    uncompleted_color = ()
    important_color = ()
    text_color = ()
    overdue_color = ()
    button_color = ()
    priority_color = ()

    tasks_to_complete_text = StringProperty()
    info_panel_text = StringProperty()
    help_content = StringProperty()
    number_of_buttons = NumericProperty()
    tasks_box_height = NumericProperty()
    help_label_height = NumericProperty()
    spinner_selections = ListProperty()
    sorting_spinner_options = ObjectProperty(SortingSpinnerOption)
    priority_spinner_options = ObjectProperty(PrioritySpinnerOption)

    def __init__(self, **kwargs):
        """Initialize TravelTrackerApp class, load tasks into task_collection from tasks.csv."""
        super().__init__(**kwargs)
        # Default loaded settings
        self.tasks_file_name = ""
        self.completed_sound = ""
        self.help_content = ""
        self.help_label_height = 0
        # Load settings
        self.load_settings()
        # Load help content
        self.load_help_content()
        # Static settings
        self.task_collection = TaskCollection()
        self.task_collection.load_tasks(self.tasks_file_name)
        self.spinner_selections = sorted(SPINNER_SELECTIONS_TO_ATTRIBUTES.keys())
        self.buttons = []
        self.priority_spinners = []
        self.sorting_is_reversed = False
        self.grouping_completed_tasks = True

    def build(self):
        """Construct the GUI, setting string and list properties to starting values."""
        self.title = "TaskTracker 2.1"
        self.icon = "icon.png"
        Window.size = (900, 650)
        self.root = Builder.load_file("app.kv")
        self.info_panel_text = "Welcome to TaskTracker 2.1!"
        self.refresh_buttons()
        return self.root

    def on_stop(self):
        """Save tasks to tasks.csv when program ends."""
        self.task_collection.save_tasks(self.tasks_file_name)

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
            self.play_sound(self.completed_sound)
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
            if task.is_completed:
                background_color = self.completed_color
            else:
                background_color = self.uncompleted_color

            task_button = ButtonBoxLayout(
                id="button_{}".format(button_number),
                background_color=background_color,
                on_release=self.mark_completed_or_uncompleted
            )
            name_label = TaskLabel(text=task.name)
            subject_label = TaskLabel(text=task.subject, size_hint_x=0.8)
            due_date_label = TaskLabel(
                text=str(task.due_date),
                size_hint_x=0.6,
                color=self.overdue_color if task.is_due() and not task.is_completed else self.text_color,
            )
            priority_spinner = PrioritySpinner(
                id="button_{}_priority".format(button_number),
                text=str(task.priority),
                background_color=background_color if not task.is_important() or task.is_completed else self.important_color,
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
        input_fields = [self.root.ids.name_input, self.root.ids.subject_input, self.root.ids.priority_input, self.root.ids.due_date_input]
        name = input_fields[0].text
        subject = input_fields[1].text
        priority = input_fields[2].text
        due_date_string = input_fields[3].text.title()
        if name and subject and priority:
            try:
                priority = int(priority)
                # Due date entered can be a date (dd/mm/yyyy), "None", or ""
                if due_date_string != "":
                    Date(due_date_string)
                else:
                    due_date_string = "None"
                if priority <= 0:
                    self.info_panel_text = "Priority must be > 0"
                else:
                    # task_collection.add_task() returns a confirmation message:
                    task = Task(name, subject, priority, due_date_string)
                    self.task_collection.add_task(task)
                    self.info_panel_text = "{} added".format(task)
                    # Utilize variable arguments to clear text of any amount of widgets
                    self.clear_widget_text(input_fields[0], input_fields[1], input_fields[2], input_fields[3])
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
            self.info_panel_text = "Completed tasks removed"
        else:
            self.info_panel_text = "No completed tasks"
        for button in self.buttons:
            if button.task.is_completed:
                self.task_collection.remove_task(button.task)
                self.root.ids.tasks_box.remove_widget(button)
                self.root.ids.tasks_box.remove_widget(self.priority_spinners[self.buttons.index(button)])

    def reverse_sorting(self):
        """Reverse the sorting of tasks."""
        self.sorting_is_reversed = not self.sorting_is_reversed
        self.info_panel_text = "Sorting reversed"
        self.refresh_buttons()

    def group_or_ungroup(self):
        """Toggle is_completed as the first sorting attribute."""
        self.grouping_completed_tasks = not self.grouping_completed_tasks
        if self.grouping_completed_tasks:
            self.info_panel_text = "Grouping on"
        else:
            self.info_panel_text = "Grouping off"
        self.refresh_buttons()

    def increment_priority(self, instance):
        """Increment task priority by an amount passed in."""
        amount = -1 if instance.text == "Up" else 1
        if amount > 0 or instance.task.priority > 1:
            instance.task.priority += amount
        self.refresh_buttons()

    @staticmethod
    def show_help_popup():
        """Display the help popup."""
        help_popup = HelpPopup(id="help_popup", title="Help", size_hint=(None, None), size=(600, 600))
        help_popup.open()

    @staticmethod
    def clear_widget_text(*widgets):
        """Clear the text of any number of any number of widgets passed in."""
        for widget in widgets:
            widget.text = ""

    @staticmethod
    def play_sound(sound):
        """Play the sound of the file passed in using playsound module."""
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound))

    def load_settings(self):
        """Read settings file and change app settings accordingly."""
        with open(SETTINGS_FILE, 'r') as file_in:
            file_in.readline()
            file_in.readline()
            file_in.readline()
            self.tasks_file_name = file_in.readline().strip()
            file_in.readline()
            file_in.readline()
            self.completed_sound = file_in.readline().strip()
            colors = []
            for line in file_in:
                line = line.strip()
                if not line:
                    continue
                elif line[0].isnumeric():  # check if line contains RGBA values
                    colors.append([round(int(value) / 255, 2) for value in line.strip().split(",")])
            self.completed_color, self.uncompleted_color, self.important_color, self.text_color, self.overdue_color, self.button_color, self.priority_color = colors

    def load_help_content(self):
        """Read help documentation from file."""
        with open(HELP_FILE, 'r') as help_file:
            for line in help_file:
                self.help_label_height += 20
                self.help_content += line


if __name__ == '__main__':
    TaskTrackerApp().run()
