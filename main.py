import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Email App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 800
    page.window_height = 600

    # Sample emails data
    emails = [
        {"sender": "John Doe", "preview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "time": "10:30 AM"},
        {"sender": "Jane Smith", "preview": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "time": "9:15 AM"},
        {"sender": "Alice Johnson", "preview": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.", "time": "Yesterday"},
        {"sender": "Bob Brown", "preview": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.", "time": "Yesterday"},
        {"sender": "Charlie Davis", "preview": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.", "time": "2 days ago"},
        {"sender": "Diana Evans", "preview": "Mollit anim id est laborum.", "time": "2 days ago"},
    ]

    # Create email list items
    email_list = ft.ListView(expand=True, spacing=0, padding=0)
    
    for email in emails:
        email_list.controls.append(
            ft.ListTile(
                title=ft.Text(email["sender"], weight=ft.FontWeight.W_600),
                subtitle=ft.Text(email["preview"], max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                trailing=ft.Text(email["time"], color=ft.colors.GREY_600),
                # padding=ft.padding.symmetric(vertical=10, horizontal=15),
                on_click=lambda e: print("Email selected"),
            )
        )
        email_list.controls.append(ft.Divider(height=1))

    # Navigation rail for inbox categories
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.INBOX_OUTLINED,
                selected_icon=ft.icons.INBOX,
                label="Inbox"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SEND_OUTLINED,
                selected_icon=ft.icons.SEND,
                label="Sent"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.STAR_OUTLINE,
                selected_icon=ft.icons.STAR,
                label="Starred"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.DELETE_OUTLINE,
                selected_icon=ft.icons.DELETE,
                label="Trash"
            ),
        ],
    )

    # Main app layout
    page.add(
        ft.Row(
            [
                # Left navigation panel
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Email App", size=20, weight=ft.FontWeight.BOLD),
                            nav_rail,
                            ft.TextField(
                                label="Search mail",
                                prefix_icon=ft.icons.SEARCH,
                                border_radius=20,
                            )
                        ],
                        spacing=0
                    ),
                    width=250,
                    bgcolor=ft.colors.GREY_100,
                ),
                
                # Right email list
                ft.Container(
                    content=email_list,
                    expand=True,
                    padding=ft.padding.only(top=20),
                )
            ],
            expand=True,
        )
    )

ft.app(target=main)