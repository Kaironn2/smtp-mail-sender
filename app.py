import flet as ft
from tab_profiles import ProfilesTab

def main(page: ft.Page):

    def snack_bar_func(text: str):
        snack_bar = ft.SnackBar(
            content=ft.Text(text),
            open=True,
            duration=2000,
            action="OK",
        )
        page.snack_bar = snack_bar
        page.overlay.append(snack_bar)
        page.update()

    page.title = 'E-mail Sender'


    profiles_tab = ProfilesTab(page, snack_bar_func).build()
    
    blacklist_tab = ft.Tab(
        text="Blacklist"
    )

    send_tab = ft.Tab(
        text="Sender"
    )

    page.add(
        ft.Tabs(
            tabs=[profiles_tab, blacklist_tab, send_tab],
        ),
    )

if __name__ == '__main__':
    ft.app(target=main)
