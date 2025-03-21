from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import database
import notifications
import threading
import time

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Chat history display
        self.chat_label = Label(text="Assistant: How can I help?\n", size_hint=(1, 0.8))
        self.add_widget(self.chat_label)

        # User input field
        self.user_input = TextInput(hint_text="Type a task...", size_hint=(1, 0.1))
        self.add_widget(self.user_input)

        # Send button
        self.send_button = Button(text="Send", size_hint=(1, 0.1))
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

        # Start background thread for reminders
        threading.Thread(target=self.check_notifications, daemon=True).start()

    def send_message(self, instance):
        text = self.user_input.text.strip()
        if text:
            self.chat_label.text += f"You: {text}\n"
            self.user_input.text = ""

            # Handling task setting
            if "reminder" in text.lower():
                parts = text.split(" at ")
                if len(parts) == 2:
                    task_name = parts[0].replace("Reminder:", "").strip()
                    task_time = parts[1].strip()
                    
                    database.add_task(task_name, task_time)
                    self.chat_label.text += f"Assistant: Task '{task_name}' set for {task_time} ✅\n"
                else:
                    self.chat_label.text += "Assistant: Use format: Reminder: Task at HH:MM\n"
            else:
                self.chat_label.text += "Assistant: I can only set reminders for now! 🕒\n"

    def check_notifications(self):
        while True:
            task = database.check_due_tasks()
            if task:
                notifications.send_notification(task)
                self.chat_label.text += f"Assistant: Reminder! {task['name']} is due now! 🔔\n"
            time.sleep(60)  # Check every minute

class StudentAssistantApp(App):
    def build(self):
        return ChatUI()

if __name__ == "__main__":
    StudentAssistantApp().run()
