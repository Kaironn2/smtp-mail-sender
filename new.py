import flet as ft
import pandas as pd
import paths

df = pd.read_csv(paths.sendedmails_csv, sep=',')

def main(page: ft.Page):
    page.title = 'Stormails'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    email_list = ft.ListView(expand=True, spacing=0, padding=ft.padding.symmetric(horizontal=16))
    shadow_config = ft.BoxShadow(blur_radius=4, spread_radius=1, color=ft.colors.BLACK12)

    for _, row in df.iterrows():
        email_list.controls.append(
            ft.Container(
                content=ft.ListTile(
                    title=ft.Text(row["from_mail"], weight=ft.FontWeight.W_600),
                    subtitle=ft.Text(row["subject"], max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    trailing=ft.Text(row["date"], color=ft.colors.GREY_600),
                    content_padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    on_click=lambda e: print("Email selected"),
                    bgcolor=ft.colors.WHITE,
                    hover_color=ft.colors.GREY_200,
                ),
                bgcolor=ft.colors.WHITE,
                border_radius=4,
                shadow=shadow_config
            )
        )
        email_list.controls.append(ft.Divider(height=20, opacity=0))


    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text('STORMAILS', size=24, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=80)
                        ],
                        spacing=0
                    ),
                    bgcolor=ft.colors.WHITE,
                    width=200,
                    padding=0,
                    shadow=shadow_config
                ),

                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text('ENVIADOS', size=20, weight=ft.FontWeight.BOLD),
                                height=80,
                                bgcolor=ft.colors.WHITE,
                                padding=ft.padding.only(left=30),
                                width=page.width - 200,
                                border_radius=1,
                                shadow=shadow_config,
                                alignment=ft.alignment.center_left
                            ),
                            ft.Container(
                                content=email_list,
                                padding=ft.padding.only(top=16),
                                expand=True
                            )
                        ],
                        expand=True,
                        spacing=0
                    ),
                    expand=True,
                    padding=0,
                )
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
