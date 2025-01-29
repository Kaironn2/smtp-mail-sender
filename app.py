import flet as ft

def main(page: ft.Page):
    
    settings_tab = ft.Tab(
        text="Settings"
    )

    blacklist_tab = ft.Tab(
        text="Blacklist"
    )

    send_tab = ft.Tab(
        text="Sender"
    )


    page.add(
        ft.Tabs(
            tabs=[settings_tab, blacklist_tab, send_tab],
        )
    )

    pass

if __name__ == '__main__':
    ft.app(target=main)
