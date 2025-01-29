import flet as ft
import json
import os

class SMTPProfiles:
    def __init__(self):
        self.profiles = self.load_profiles()
        self.current_profile = None

    def load_profiles(self):
        try:
            if os.path.exists("smtp_profiles.json"):
                with open("smtp_profiles.json", "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading profiles: {e}")
            return {}

    def save_profiles(self):
        with open("smtp_profiles.json", "w") as f:
            json.dump(self.profiles, f)

class ProfileTab(ft.UserControl):
    def __init__(self, profiles_manager):
        super().__init__()
        self.profiles = profiles_manager
        self.profile_name = ft.TextField(label="SMTP Profile Name")
        self.smtp_server = ft.TextField(label="SMTP Server")
        self.smtp_port = ft.TextField(label="SMTP Port")
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.profiles_list = ft.ListView(expand=True)

    def build(self):
        return ft.Tab(
            text="SMTP Profiles",
            content=ft.Row(
                [
                    self._build_edit_column(),
                    self._build_profiles_column()
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        )

    def _build_edit_column(self):
        return ft.Column(
            [
                self.profile_name,
                self.smtp_server,
                self.smtp_port,
                self.username,
                self.password,
                ft.ElevatedButton(
                    "Save Profile",
                    on_click=self._save_profile,
                    icon=ft.icons.SAVE
                )
            ],
            width=400,
            spacing=15
        )

    def _build_profiles_column(self):
        return ft.Column(
            [
                ft.Text("Existing Profiles:", weight=ft.FontWeight.BOLD),
                self.profiles_list
            ],
            width=400,
            spacing=10
        )

    def _save_profile(self, e):
        profile_data = {
            "name": self.profile_name.value.strip(),
            "server": self.smtp_server.value.strip(),
            "port": self.smtp_port.value.strip(),
            "username": self.username.value.strip(),
            "password": self.password.value.strip()
        }

        if not all(profile_data.values()):
            self.page.snack_bar = ft.SnackBar(ft.Text("All fields are required!"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.profiles.profiles[profile_data["name"]] = profile_data
        self.profiles.save_profiles()
        self._clear_fields()
        self._update_profiles_list()
        self.page.update()

    def _edit_profile(self, profile_name):
        profile = self.profiles.profiles[profile_name]
        self.profile_name.value = profile["name"]
        self.smtp_server.value = profile["server"]
        self.smtp_port.value = profile["port"]
        self.username.value = profile["username"]
        self.password.value = profile["password"]
        self.profiles.current_profile = profile_name
        self.page.update()

    def _delete_profile_dialog(self, profile_name):
        def close_dlg(e):
            dlg.open = False
            self.page.update()

        def confirm_delete(e):
            del self.profiles.profiles[profile_name]
            self.profiles.save_profiles()
            self._update_profiles_list()
            close_dlg(e)

        dlg = ft.AlertDialog(
            title=ft.Text(f"Delete {profile_name}?"),
            content=ft.Text("This action cannot be undone!"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton(
                    "Delete",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color=ft.colors.RED)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _clear_fields(self):
        self.profile_name.value = ""
        self.smtp_server.value = ""
        self.smtp_port.value = ""
        self.username.value = ""
        self.password.value = ""
        self.profiles.current_profile = None
        self.page.update()

    def _update_profiles_list(self):
        self.profiles_list.controls.clear()
        for name in self.profiles.profiles:
            self.profiles_list.controls.append(
                ft.Row(
                    [
                        ft.Text(name),
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Edit",
                            on_click=lambda e, n=name: self._edit_profile(n)
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, n=name: self._delete_profile_dialog(n)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        self.page.update()

    def did_mount(self):
        self._update_profiles_list()

def main(page: ft.Page):
    page.title = "SMTP Profile Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.add(
        ft.Tabs(
            tabs=[ProfileTab(SMTPProfiles()).build()],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)