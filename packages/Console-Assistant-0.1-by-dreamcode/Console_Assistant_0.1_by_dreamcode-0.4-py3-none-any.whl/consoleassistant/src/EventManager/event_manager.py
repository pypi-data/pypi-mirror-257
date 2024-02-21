from src.View.base_view import ConsoleView
from src.tools.common import CommandHandler, handle_error
from datetime import datetime, timedelta
import json


class Event:
    """
    Class to represent an event.
    """
    def __init__(self, title, date_time, tags=None):
        """
        Initialize the event object.

        :param title: Title of the event.
        :param date_time: Date and time of the event.
        :param tags: Tags associated with the event (default is None).
        """
        self.title = title
        self.date_time = date_time
        self.tags = tags or []

    def time_until_event(self):
        """
        Calculate the time until the event occurs.

        :return: Time until the event.
        """
        return self.date_time - datetime.now()

    def __str__(self):
        """
        Return a string representation of the event.

        :return: String representation of the event.
        """
        return f'Title: {self.title}\nDate and Time: {self.date_time}\nTags: {", ".join(self.tags)}\n'


class EventManager:
    """
    Class to manage events.
    """
    def __init__(self, file_path, view):
        """
        Initialize the event manager.

        :param file_path: Path to the file where events are stored.
        :param view: View object for interacting with the user.
        """
        self.file_path = file_path
        self.events = self.load_events()
        self.view = view

    def load_events(self):
        """
        Load events from a file.

        :return: List of events.
        """
        try:
            with open(self.file_path, 'r') as file:
                events_data = json.load(file, object_hook=self.event_decoder)
                events = [Event(**event_data) for event_data in events_data]
                return events
        except FileNotFoundError:
            return []

    def event_decoder(self, obj):
        if 'date_time' in obj:
            obj['date_time'] = datetime.strptime(obj['date_time'], '%Y-%m-%d %H:%M')
        return obj

    def save_events(self):
        events_data = []
        for event in self.events:
            event_data = event.__dict__.copy()
            event_data['date_time'] = event.date_time.strftime('%Y-%m-%d %H:%M')
            events_data.append(event_data)
        with open(self.file_path, 'w') as file:
            json.dump(events_data, file, indent=4)

    @handle_error
    def add_event(self):
        title = self.view.get_input('Enter event title: ')
        while True:
            date_time_str = self.view.get_input('Enter event date and time (YYYY-MM-DD HH:MM): ')
            try:
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                break
            except ValueError:
                self.view.display_message('Please enter date and time in the format YYYY-MM-DD HH:MM.')
        tags = self.view.get_input('Enter tags separated by commas: ').split(',')
        event = Event(title, date_time, tags)
        self.events.append(event)
        self.save_events()
        self.view.display_message('Event added successfully.')

    def search_event(self):
        title = self.view.get_input('Enter event title to search: ')
        found_events = [event for event in self.events if event.title.lower() == title.lower()]
        if found_events:
            self.view.display_message(f"Found {len(found_events)} event(s) with title '{title}':")
            for event in found_events:
                self.view.display_message(str(event))
        else:
            self.view.display_message(f"No events found with title '{title}'.")

    def edit_event(self):
        title = self.view.get_input('Enter event title to edit: ')
        for event in self.events:
            if event.title == title:
                new_title = self.view.get_input('Enter new event title: ')
                while True:
                    new_date_time_str = self.view.get_input('Enter new event date and time (YYYY-MM-DD HH:MM): ')
                    try:
                        new_date_time = datetime.strptime(new_date_time_str, '%Y-%m-%d %H:%M')
                        break
                    except ValueError:
                        self.view.display_message('Please enter date and time in the format YYYY-MM-DD HH:MM.')
                new_tags = self.view.get_input('Enter new tags separated by commas: ').split(',')
                event.title = new_title
                event.date_time = new_date_time
                event.tags = new_tags
                self.view.display_message('Event edited successfully.')
                self.save_events()
                return
        self.view.display_message(f'Event with title "{title}" not found.')

    def delete_event(self):
        title = self.view.get_input('Enter event title to delete: ')
        for event in self.events:
            if event.title == title:
                self.events.remove(event)
                self.view.display_message('Event deleted successfully.')
                self.save_events()
                return
        self.view.display_message(f'Event with title "{title}" not found.')

    @handle_error
    def show_upcoming_events(self):
        today = datetime.now()
        upcoming_events = [event for event in self.events if event.time_until_event() <= timedelta(days=7)]
        if upcoming_events:
            sorted_upcoming_events = sorted(upcoming_events, key=lambda event: event.date_time)
            self.view.display_message('Upcoming events within a week:')
            for event in sorted_upcoming_events:
                self.view.display_message(str(event))
        else:
            self.view.display_message('No upcoming events within a week.')

    @handle_error
    def show_all_events(self):
        if not self.events:
            self.view.display_message('No events found.')
            return
        sorted_events = sorted(self.events, key=lambda event: event.date_time)
        self.view.display_message('All events:')
        for event in sorted_events:
            self.view.display_message(str(event))


class EventCommandHandler(CommandHandler):
    """
    Class to handle event commands.
    """

    def __init__(self, manager, view):
        """
        Initialize the command handler.

        :param manager: Event manager.
        :param view: View object for interacting with the user.
        """
        commands = {
            "1": ("Add event", manager.add_event),
            "2": ("Show upcoming events", manager.show_upcoming_events),
            "3": ("Show all events", manager.show_all_events),
            "4": ("Search event", manager.search_event),
            "5": ("Edit event", manager.edit_event),
            "6": ("Delete event", manager.delete_event),
            "0": ("Return to Main Menu", self.return_to_main_menu())
        }
        super().__init__(commands, view)
        self.manager = manager

    def handle_command(self, choice):
        """
        Handle the selected command.

        :param choice: User's choice of command.
        """
        command = self.commands.get(choice)
        if command:
            command[1]()
        else:
            self.view.display_message('Invalid choice. Please select a valid option.')

    def return_to_main_menu(self):
        """
        Return to the main menu.
        """
        return


def run_event_manager():
    """
    Runs the event manager application.
    """
    program_name = "Event Manager V0.1"
    event_file_path = 'events.json'
    view = ConsoleView()
    event_manager = EventManager(event_file_path, view)
    event_command_handler = EventCommandHandler(event_manager, view)

    while True:
        options = {
            '1': 'Add event',
            '2': 'Show upcoming events',
            '3': 'Show all events',
            '4': 'Search event',
            '5': 'Edit event',
            '6': 'Delete event',
            '0': 'Return to Main Menu'
        }
        choice = view.display_menu(program_name, options)
        if choice in ['1', '2', '3', '4', '5', '6']:

            event_command_handler.handle_command(choice)
        elif choice == '0':
            event_manager.save_events()
            return
        else:
            view.display_message('Invalid choice. Please select a valid option.')


if __name__ == '__main__':
    run_event_manager()
