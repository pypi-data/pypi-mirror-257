from datetime import date
from src.View.base_view import ConsoleView
from src.tools.common import CommandHandler, handle_error
import json


class Note:
    """
    Represents a note with title, content, and tags.

    Attributes:
        title (str): The title of the note.
        content (str): The content of the note.
        tags (list): The tags associated with the note.
    """
    def __init__(self, title, content, tags, note_date=None):
        """
        Initializes a Note object with the provided title, content, and tags.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags (list): The tags associated with the note.
        """
        self.title = title
        self.tags = tags
        self.content = content
        if note_date:
            self.note_date = note_date
        else:
            self.note_date = date.today().strftime("%d-%m-%Y")

    def __str__(self):
        """
        Returns a string representation of the note.

        Returns:
            str: A string containing the title, tags, and content of the note.
        """
        return f"Title: {self.title}\nTags: {', '.join(self.tags)}\nContent: {self.content}\nDate: {self.note_date}"


class NoteManager:
    """
    Manages notes, including loading, saving, adding, searching, editing, deleting,
    adding tags, and displaying all notes.

    Attributes:
        file_path (str): The file path to store notes.
        notes (list): A list of Note objects representing the notes.
        view: The view object for input/output.
    """
    def __init__(self, file_path, view):
        """
        Initializes a NoteManager object with the provided file path and view.

        Args:
            file_path (str): The file path to store notes.
            view: The view object for input/output.
        """
        self.file_path = file_path
        self.notes = self.load_notes()
        self.view = view

    def load_notes(self):
        """
        Loads notes from a JSON file.

        Returns:
            list: A list of Note objects representing the loaded notes.
        """
        try:
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(**note_data) for note_data in notes_data]
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        """
        Saves notes to a JSON file.
        """
        notes_data = [note.__dict__ for note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file, indent=4)

    @handle_error
    def add_note(self):
        """
        Adds a new note.
        """
        title = self.view.get_input('Enter note title: ')
        content = self.view.get_input('Enter note content: ')
        tags = self.view.get_input('Enter tags separated by commas: ').split(',')
        note = Note(title, content, tags)
        self.notes.append(note)
        self.save_notes()
        self.view.display_message('Note added successfully.')

    @handle_error
    def search_note(self):
        """
        Searches for notes based on a query.
        """
        query = self.view.get_input('Enter search query: ')
        results = [note for note in self.notes if query in note.title or query in note.content\
                   or query in note.tags or query in note.note_date]
        if results:
            sorted_results = sorted(results, key=lambda note: note.title)
            self.view.display_message('Search results:')
            for note in sorted_results:
                self.view.display_message(str(note))
        else:
            self.view.display_message('No notes found matching the query.')

    @handle_error
    def edit_note(self):
        """
        Edits an existing note.
        """
        title = self.view.get_input('Enter the title of the note you want to edit: ')
        new_content = self.view.get_input('Enter the new content for the note: ')
        for note in self.notes:
            if note.title == title:
                note.content = new_content
                self.save_notes()
                self.view.display_message('Note successfully edited.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def delete_note(self):
        """
        Deletes an existing note.
        """
        title = self.view.get_input('Enter the title of the note you want to delete: ')
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                self.save_notes()
                self.view.display_message('Note successfully deleted.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def add_tag_to_note(self):
        """
        Adds a tag to an existing note.
        """
        title = self.view.get_input('Enter the title of the note to which you want to add a tag: ')
        tag = self.view.get_input('Enter the tag: ')
        for note in self.notes:
            if note.title == title:
                note.tags.append(tag)
                self.save_notes()
                self.view.display_message('Tag successfully added to the note.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def show_all_notes(self):
        """
        Displays all notes.
        """
        if not self.notes:
            self.view.display_message('No notes found.')
            return
        sorted_notes = sorted(self.notes, key=lambda note: note.title)
        self.view.display_message('All notes:')
        for note in sorted_notes:
            self.view.display_message(str(note))


class NoteCommandHandler(CommandHandler):
    """
    Handles commands for notes, such as adding, searching, editing, deleting,
    adding tags, and showing all notes.

    Attributes:
        manager: The NoteManager object to perform note-related operations.
        view: The view object for input/output.
    """
    def __init__(self, manager, view):
        """
        Initializes a NoteCommandHandler object with the provided NoteManager object and view.

        Args:
            manager: The NoteManager object to perform note-related operations.
            view: The view object for input/output.
        """
        super().__init__(manager, view)
        commands = {
            "1": ("Add note", manager.add_note),
            "2": ("Search note", manager.search_note),
            "3": ("Edit note", manager.edit_note),
            "4": ("Delete note", manager.delete_note),
            "5": ("Add tag to note", manager.add_tag_to_note),
            "6": ("Show all notes", manager.show_all_notes),
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


def run_note_manager():
    """
    Runs the note manager application.
    """
    program_name = "Note Manager V0.1"
    note_file_path = 'notes.json'
    view = ConsoleView()
    manager = NoteManager(note_file_path, view)
    note_command_handler = NoteCommandHandler(manager, view)

    while True:
        options = {
            '1': 'Add note',
            '2': 'Search note',
            '3': 'Edit note',
            '4': 'Delete note',
            '5': 'Add tag to note',
            '6': 'Show all notes',
            '0': 'Return to Main Menu'
        }
        choice = view.display_menu(program_name, options)
        if choice in ['1', '2', '3', '4', '5', '6']:
            note_command_handler.handle_command(choice)
        elif choice == '0':
            return
        else:
            view.display_message('Invalid choice. Please select a valid option.')


if __name__ == '__main__':
    run_note_manager()
