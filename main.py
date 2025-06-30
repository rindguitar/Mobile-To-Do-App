# main.py - To-Doアプリの基本構造

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
import sqlite3
from datetime import datetime


class TodoDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_table()
    
    def create_table(self):
        """テーブル作成"""
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
        """タスク追加"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date)
            VALUES (?, ?, ?)
        ''', (title, description, due_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_tasks(self):
        """全タスク取得"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        return cursor.fetchall()
    
    def delete_task(self, task_id):
        """タスク削除"""
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
        
        # データベース初期化
        self.db = TodoDatabase()
        
        # UI要素作成
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        """UI要素を作成"""
        # タイトル
        title = MDLabel(
            text="To-Do タスク管理",
            theme_text_color="Primary",
            size_hint_y=None,
            height="48dp",
            font_style="H4"
        )
        self.add_widget(title)
        
        # タスク入力フィールド
        self.task_input = MDTextField(
            hint_text="新しいタスクを入力",
            size_hint_y=None,
            height="56dp"
        )
        self.add_widget(self.task_input)
        
        # 追加ボタン
        add_button = MDRaisedButton(
            text="タスク追加",
            size_hint_y=None,
            height="40dp",
            on_release=self.add_task
        )
        self.add_widget(add_button)
        
        # タスクリスト
        self.task_list = MDList()
        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        self.add_widget(scroll)
    
    def add_task(self, instance):
        """タスクを追加"""
        task_text = self.task_input.text.strip()
        if task_text:
            # データベースに追加
            self.db.add_task(task_text)
            
            # 入力フィールドをクリア
            self.task_input.text = ""
            
            # リスト更新
            self.refresh_task_list()
    
    def refresh_task_list(self):
        """タスクリストを更新"""
        # リストをクリア
        self.task_list.clear_widgets()
        
        # データベースからタスクを取得
        tasks = self.db.get_all_tasks()
        
        # リストに追加
        for task in tasks:
            task_id, title, description, due_date, is_completed, created_at = task
            
            # リストアイテム作成
            item = OneLineListItem(
                text=f"{title}",
                on_release=lambda x, task_id=task_id: self.delete_task(task_id)
            )
            self.task_list.add_widget(item)
    
    def delete_task(self, task_id):
        """タスクを削除"""
        self.db.delete_task(task_id)
        self.refresh_task_list()


class TodoApp(MDApp):
    def build(self):
        # テーマ設定
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        return MainScreen()


if __name__ == "__main__":
    TodoApp().run()