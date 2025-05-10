import flet as ft
from database import Database, Event

class PublicEventsContainer(ft.Container):
    def __init__(self, page: ft.Page):
        self.name = "Public Events"

        db = Database("events-users")
        events = db.get_events()

        events_display = ft.Column()
        for event in events:
            n_participants = len(db.get_participants(event.id))
            events_display.controls.append(
                SingleEventContainer(
                    event,
                    n=n_participants,
                    on_click=lambda e: page.go(f"/event/{e.control.id}"),
                )
            )

        super().__init__(
            content=events_display,
        )



class SingleEventContainer(ft.Container):
    def __init__(self, event: Event, n: int, on_click: callable = None):
        self.id = event.id
        n_text = "1 Pal" if n == 0 else f"{n+1} Pals"

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                ft.Text(event.name, size=16, color=ft.Colors.ON_PRIMARY),
                                bgcolor=ft.Colors.ON_PRIMARY_CONTAINER,
                                padding=5,
                                margin=0,
                                border_radius=5,
                            ),
                            ft.Container(
                                ft.Text(n_text, size=16, color=ft.Colors.ON_PRIMARY),
                                bgcolor=ft.Colors.ON_PRIMARY_CONTAINER,
                                padding=5,
                                margin=0,
                                border_radius=5,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text("Where: " + event.location),
                    ft.Text("When: " + event.date),
                    ft.Text("At: " + event.time),
                    ft.Text("Description: " + event.description),
                ],
            ),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            padding=10,
            margin=5,
            border_radius=10,
            on_click=on_click,
        )