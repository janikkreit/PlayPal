import flet as ft

from database import Event, Database

class CreateEventView(ft.View):
    def __name__(self):
        return "Create Event"

    def __init__(self, page: ft.Page):
        self.page = page

        self.fields = [
            ft.TextField(label="Event Name", autofocus=True),
            ft.TextField(label="Location"),
            ft.TextField(label="Date"),
            ft.TextField(label="Time"),
            ft.TextField(label="Description"),
        ]

        appbar = ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: self.page.go("/")),
            title=ft.Text("Create Event"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        )

        super().__init__(
            route="/create",
            controls=[
                ft.Column(
                    self.fields + [
                        ft.ElevatedButton("Create Event", on_click=self.submit_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            appbar=appbar,
        )


    def submit_click(self, e):
        data = {}
        for field in self.fields:
            if field.value == "":
                self.page.open(ft.SnackBar(ft.Text("Please fill all fields")))
                return
            data[field.label] = field.value

        # print(data, **data)

        db = Database("events-users")
        db.add_event(Event(
            name=data["Event Name"],
            location=data["Location"],
            date=data["Date"],
            time=data["Time"],
            description=data["Description"],
            owner_id=self.page.session.get("user_id")),
        )


        self.snackbar = ft.SnackBar(ft.Text("Event created successfully!"), open=True)
        self.page.go("/")