# main.py - To-Do App Basic Structure

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.pickers import MDDatePicker
import sqlite3
from datetime import datetime
import os


class TodoDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_table()
    
    def create_table(self):
        """Create table"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                is_completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_task(self, title, description="", due_date=""):
        """Add task"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date)
            VALUES (?, ?, ?)
        ''', (title, description, due_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_tasks(self):
        """Get all tasks"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        return cursor.fetchall()
    
    def delete_task(self, task_id):
        """Delete task"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()


class MainScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.adaptive_height = True
        self.padding = "20dp"
        
        # Initialize database
        self.db = TodoDatabase()
        
        # Store selected date
        self.selected_date = None
        
        # Create UI elements
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        """Create UI elements"""
        # Title
        title = MDLabel(
            text="To-Do Task Manager",
            theme_text_color="Primary",
            size_hint_y=None,
            height="48dp",
            font_style="H4"
        )
        self.add_widget(title)
        
        # Task input field
        self.task_input = MDTextField(
            hint_text="Enter new task",
            size_hint_y=None,
            height="56dp"
        )
        self.add_widget(self.task_input)
        
        # Date selection section
        date_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="48dp",
            spacing="12dp"
        )
        
        # Date display label
        self.date_label = MDLabel(
            text="No date selected",
            size_hint_x=0.7,
            theme_text_color="Secondary"
        )
        date_layout.add_widget(self.date_label)
        
        # Date selection button
        date_button = MDIconButton(
            icon="calendar",
            on_release=self.open_date_picker
        )
        date_layout.add_widget(date_button)
        
        # Date clear button
        clear_date_button = MDIconButton(
            icon="close",
            on_release=self.clear_date
        )
        date_layout.add_widget(clear_date_button)
        
        self.add_widget(date_layout)
        
        # Add button
        add_button = MDRaisedButton(
            text="Add Task",
            size_hint_y=None,
            height="40dp",
            on_release=self.add_task
        )
        self.add_widget(add_button)
        
        # Task list
        self.task_list = MDList()
        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        self.add_widget(scroll)
    
    def add_task(self, instance):
        """Add task"""
        task_text = self.task_input.text.strip()
        if task_text:
            # Prepare date as string
            due_date = self.selected_date.strftime("%Y-%m-%d") if self.selected_date else ""
            
            # Add to database
            self.db.add_task(task_text, due_date=due_date)
            
            # Clear input field
            self.task_input.text = ""
            self.selected_date = None
            self.date_label.text = "No date selected"
            
            # Update list
            self.refresh_task_list()
    
    def open_date_picker(self, instance):
        """Open date picker dialog"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
    
    def get_date(self, instance, value, date_range):
        """Get selected date"""
        self.selected_date = value
        self.date_label.text = f"Due: {value.strftime('%Y-%m-%d')}"
    
    def clear_date(self, instance):
        """Clear date selection"""
        self.selected_date = None
        self.date_label.text = "No date selected"
    
    def refresh_task_list(self):
        """Update task list"""
        # Clear list
        self.task_list.clear_widgets()
        
        # Get tasks from database
        tasks = self.db.get_all_tasks()
        
        # Add to list
        for task in tasks:
            task_id, title, description, due_date, is_completed, created_at = task
            
            # Add date information
            display_text = title
            if due_date:
                try:
                    date_obj = datetime.strptime(due_date, "%Y-%m-%d")
                    display_text += f" (Due: {date_obj.strftime('%m/%d')})"
                except ValueError:
                    pass
            
            # Create list item
            item = OneLineListItem(
                text=display_text,
                on_release=lambda x, task_id=task_id: self.delete_task(task_id)
            )
            self.task_list.add_widget(item)
    
    def delete_task(self, task_id):
        """Delete task"""
        self.db.delete_task(task_id)
        self.refresh_task_list()


class TodoApp(MDApp):
    def build(self):
        # Theme settings
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        return MainScreen()


if __name__ == "__main__":
    TodoApp().run()