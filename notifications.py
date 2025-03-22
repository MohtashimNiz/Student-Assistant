import platform

def send_notification(task):
    """Displays a notification for the given task."""
    message = f"Reminder: {task['name']} is due now! 🔔"

    if platform.system() == "Windows":
        from plyer import notification
        notification.notify(
            title="Student Assistant",
            message=message,
            timeout=5  # Notification disappears after 5 seconds
        )
    elif platform.system() == "Linux":
        import os
        os.system(f'notify-send "Student Assistant" "{message}"')
    elif platform.system() == "Darwin":  # macOS
        import os
        os.system(f'osascript -e \'display notification "{message}" with title "Student Assistant"\'')
    else:
        print(f"🔔 {message}")  # Fallback for unsupported systems
