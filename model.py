import os
import json
import smtplib
import logging
import threading
from datetime import datetime
import flet as ft
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(
    filename=os.path.join('logs', 'email_log.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AppState:
    def __init__(self):
        self.current_preset = self.load_presets()
        self.email_queue = []
        self.blacklist = self.load_blacklist()
        
    def load_blacklist(self):
        try:
            with open('blacklist.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'unsubscribed': [], 'full_mailbox': [], 'nonexistent': []}
            
    def save_blacklist(self):
        with open('blacklist.json', 'w') as f:
            json.dump(self.blacklist, f)
            
    def load_presets(self):
        try:
            with open(os.path.join('presets', 'preset.json')) as f:
                return json.load(f)
        except FileNotFoundError:
            return {'smtp_server': '', 'port': '', 'username': '', 'password': ''}

def main(page: ft.Page):
    def create_directories():
        os.makedirs('templates', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('presets', exist_ok=True)
    
    create_directories()
    app_state = AppState()
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.title = "Email Sender"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Settings Tab Components
    smtp_server = ft.TextField(label="SMTP Server", value=app_state.current_preset.get('smtp_server', ''))
    port = ft.TextField(label="Port", value=app_state.current_preset.get('port', ''))
    username = ft.TextField(label="Username", value=app_state.current_preset.get('username', ''))
    password = ft.TextField(label="Password", password=True, value=app_state.current_preset.get('password', ''))
    
    # Blacklist Tab Components
    blacklist_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(c) for c in app_state.blacklist.keys()],
        value=next(iter(app_state.blacklist.keys()), None)
    )
    blacklist_entry = ft.TextField(label="Email", expand=True)
    blacklist_list = ft.ListView(expand=True)
    
    # Send Tab Components
    queue_list = ft.ListView(expand=True)
    progress_bar = ft.ProgressBar(width=400, value=0)

    def update_blacklist_display():
        category = blacklist_dropdown.value
        blacklist_list.controls.clear()
        if category:
            for email in app_state.blacklist[category]:
                blacklist_list.controls.append(
                    ft.Row([
                        ft.Text(email),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda _, e=email: remove_from_blacklist(e)
                        )
                    ])
                )
        blacklist_list.update()

    def add_to_blacklist(e):
        email = blacklist_entry.value.strip()
        category = blacklist_dropdown.value
        if email and category and email not in app_state.blacklist[category]:
            app_state.blacklist[category].append(email)
            app_state.save_blacklist()
            blacklist_entry.value = ""
            update_blacklist_display()
            page.update()

    def remove_from_blacklist(email):
        category = blacklist_dropdown.value
        if category and email in app_state.blacklist[category]:
            app_state.blacklist[category].remove(email)
            app_state.save_blacklist()
            update_blacklist_display()
            page.update()

    def save_preset(e):
        app_state.current_preset = {
            'smtp_server': smtp_server.value,
            'port': port.value,
            'username': username.value,
            'password': password.value
        }
        try:
            with open(os.path.join('presets', 'preset.json'), 'w') as f:
                json.dump(app_state.current_preset, f)
            show_dialog("Success", "Preset saved successfully")
        except Exception as ex:
            show_dialog("Error", str(ex))

    def handle_file_import(e: ft.FilePickerResultEvent, file_type):
        if e.files:
            try:
                df = pd.read_csv(e.files[0].path) if file_type == 'csv' else pd.read_excel(e.files[0].path)
                if 'template' not in df.columns or 'recipient' not in df.columns:
                    show_dialog("Error", "File must contain 'template' and 'recipient' columns")
                    return
                app_state.email_queue = df.to_dict('records')
                update_queue_display()
                page.update()
            except Exception as ex:
                show_dialog("Error", str(ex))

    def update_queue_display():
        queue_list.controls.clear()
        for item in app_state.email_queue:
            queue_list.controls.append(ft.Text(f"{item['recipient']} - {item['template']}"))
        queue_list.update()

    def start_sending(e):
        required_fields = ['smtp_server', 'port', 'username', 'password']
        if any(not app_state.current_preset.get(field) for field in required_fields):
            show_dialog("Error", "Complete all SMTP settings first")
            return
        if not app_state.email_queue:
            show_dialog("Warning", "No emails in queue")
            return
        
        progress_bar.value = 0
        progress_bar.max = len(app_state.email_queue)
        page.update()

        def send_emails():
            for i, email_data in enumerate(app_state.email_queue):
                if is_blacklisted(email_data['recipient']):
                    continue
                try:
                    send_email(email_data)
                    logging.info(f"Sent {email_data['template']} to {email_data['recipient']}")
                except Exception as e:
                    logging.error(f"Failed to send to {email_data['recipient']}: {str(e)}")
                
                current_progress = i + 1
                page.run_task(lambda: update_progress(current_progress))

        threading.Thread(target=send_emails, daemon=True).start()

    def update_progress(value):
        progress_bar.value = value
        page.update()

    def send_email(email_data):
        template_path = os.path.join('templates', f"{email_data['template']}.html")
        with open(template_path) as f:
            html = f.read()
        
        for key, value in email_data.items():
            if key not in ['template', 'recipient']:
                html = html.replace(f'[[{key}]]', str(value))
        
        msg = MIMEMultipart()
        msg['From'] = app_state.current_preset['username']
        msg['To'] = email_data['recipient']
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP_SSL(
            app_state.current_preset['smtp_server'],
            int(app_state.current_preset['port'])
        ) as server:
            server.login(
                app_state.current_preset['username'],
                app_state.current_preset['password']
            )
            server.send_message(msg)

    def is_blacklisted(email):
        return any(email in category for category in app_state.blacklist.values())

    def cancel_sending(e):
        app_state.email_queue = []
        progress_bar.value = 0
        update_queue_display()
        page.update()

    def show_dialog(title, message):
        page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            on_dismiss=lambda e: page.update()
        )
        page.dialog.open = True
        page.update()

    # Assemble UI
    settings_tab = ft.Tab(
        text="Settings",
        content=ft.Column([
            smtp_server,
            port,
            username,
            password,
            ft.ElevatedButton("Save Preset", on_click=save_preset)
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )

    blacklist_tab = ft.Tab(
        text="Blacklist",
        content=ft.Column([
            blacklist_dropdown,
            ft.Row([blacklist_entry, ft.ElevatedButton("Add", on_click=add_to_blacklist)]),
            blacklist_list
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )

    send_tab = ft.Tab(
        text="Send Emails",
        content=ft.Column([
            ft.Row([
                ft.ElevatedButton(
                    "Import CSV",
                    on_click=lambda e: file_picker.pick_files(
                        allowed_extensions=['csv'],
                        on_result=lambda e: handle_file_import(e, 'csv')
                    )
                ),
                ft.ElevatedButton(
                    "Import Excel",
                    on_click=lambda e: file_picker.pick_files(
                        allowed_extensions=['xlsx', 'xls'],
                        on_result=lambda e: handle_file_import(e, 'excel')
                    )
                )
            ]),
            queue_list,
            progress_bar,
            ft.Row([
                ft.ElevatedButton("Start Sending", on_click=start_sending),
                ft.ElevatedButton("Cancel", on_click=cancel_sending)
            ])
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )

    page.add(ft.Tabs(
        tabs=[settings_tab, blacklist_tab, send_tab],
        expand=True
    ))
    update_blacklist_display()

if __name__ == "__main__":
    ft.app(target=main)