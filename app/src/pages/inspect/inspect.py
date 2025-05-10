import flet as ft

from database import Database

class InspectEventView(ft.View):
    def __name__(self):
        return "Inspect Event"

    def __init__(self, page: ft.Page, event_id: int):
        self.page = page
        self.event_id = event_id

        # Placeholder for event data
        db = Database("events-users")
        self.event_data = db.get_event_by_id(event_id)
        owner_username = db.get_user_by_id(self.event_data.owner_id).username

        appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/")),
            toolbar_height=80,
            title=ft.Text("Event Details"),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Delete Event",
                    on_click=lambda e: self.delete_clicked(self.event_id),
                ),
            ]
        )

        self.join_button = ft.ElevatedButton(
            "Join Event",
            on_click=self.join_clicked,
        )

        if self.event_data.owner_id == page.session.get("user_id"):
            self.join_button.disabled = True

        participants = db.get_participants(self.event_id)
        self.participants_row = ft.Row(
            [ft.FilledButton(owner_username + " (Owner)")],
            wrap=True,
        )
        for participant in participants:
            participant_username = db.get_user_by_id(participant.id).username
            self.participants_row.controls.append(
                ft.FilledButton(participant_username)
            )

        super().__init__(
            route=f"/event/{event_id}",
            controls=[
                ft.Column(
                    [
                        ft.Text(self.event_data.name, size=30),
                        ft.Text(f"Location: {self.event_data.location}"),
                        ft.Text(f"When: {self.event_data.date}"),
                        ft.Text(f"At: {self.event_data.time}"),
                        ft.Text(f"Description: {self.event_data.description}"),
                        self.participants_row,
                        self.join_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            appbar=appbar,
        )


    def delete_clicked(self, id):
        db = Database("events-users")
        db.delete_event(id)
        self.page.go("/")

    def join_clicked(self, e):
        db = Database("events-users")
        
        participants = db.get_participants(self.event_id)
        user_id = self.page.session.get("user_id")
        if user_id in [p.id for p in participants]:
            return

        db.add_participant(self.event_id, user_id)
        self.participants_row.controls.append(
            ft.FilledButton(
                db.get_user_by_id(user_id).username
            )
        )
        self.join_button.disabled = True
        self.update()