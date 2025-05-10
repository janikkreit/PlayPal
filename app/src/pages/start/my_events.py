import flet as ft


class MyEventsContainer(ft.Container):
    def __init__(self, page: ft.Page):
        self.name = "My Events"
        self.content = ft.Text("My Events Page")