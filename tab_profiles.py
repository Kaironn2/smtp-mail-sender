import flet as ft

class ProfilesTab():
    def __init__(self, page, snack_bar_func):
        super().__init__()
        self.page = page
        self.snack_bar_func = snack_bar_func
        self.smtp_profile_name = ft.TextField(label="SMTP Profile Name")
        self.smtp_server = ft.TextField(label="SMTP Server")
        self.port = ft.TextField(label="Port")
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.profiles_list = ft.ListView(expand=True)
        
    def build(self):
        return ft.Tab(
            text="Profiles",
            content=ft.Row(
                [
                    self._build_first_column(),
                    self._build_second_column()
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )
    
    def _build_first_column(self):
        return ft.Column(
            [
                self.smtp_profile_name,
                self.smtp_server,
                self.port,
                self.username,
                self.password,
                ft.ElevatedButton(
                    "Save Profile",
                    on_click=self._save_profile,
                    icon=ft.icons.SAVE
                )
            ],
            width=600,
            spacing=15
        )
    
    def _build_second_column(self):
        return ft.Column(
            [
                ft.Text("Existing Profiles", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                self.profiles_list,
                
            ],
            width=400,
            spacing=10,
        )
    
    def _save_profile(self, e):


        if not all([self.smtp_profile_name.value, self.smtp_server.value, self.port.value, self.username.value, self.password.value]):
            self.snack_bar_func('All fields are required')
            print('Chegou no erro all fields are required')
            return
        

        new_profile = ft.Text(self.smtp_profile_name.value)
        self.profiles_list.controls.append(new_profile)
        self.profiles_list.update()
        self.snack_bar_func('Profile Saved')
        print('Chegou no Profile Saved')

    def _reset_settings(self, e):
        pass