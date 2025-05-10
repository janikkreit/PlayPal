import flet as ft
import logging

from .my_events import MyEventsContainer
from .public_events import PublicEventsContainer
from .profile import ProfileContainer

logger = logging.getLogger("frontend")

class StartView(ft.View):
    def __name__(self):
        return "StartView"
    
    def __init__(self, page: ft.Page):
        self.page = page

        # start page
        start_page = PublicEventsContainer(page)

        # app bar
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.SPORTS_FOOTBALL),
            # leading=logo_img,
            leading_width=40,
            toolbar_height=80,
            title=ft.Text(start_page.name),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
            ],
        )

        # add navigation bar
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Public Events"),
                ft.NavigationBarDestination(icon=ft.Icons.BOOKMARK, label="My Events"),
                ft.NavigationBarDestination(icon=ft.Icons.MAN, label="Profile")
            ],
            on_change=self.nav_change,
            selected_index=0,
        )

        # add floating action button
        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda e: page.go("/create"),
        )

        logger.info("StartView initialized")

        super().__init__(
            route="/",
            appbar=self.appbar,
            navigation_bar=self.navigation_bar,
            floating_action_button=self.floating_action_button,
            controls=[start_page.content],
            scroll="adaptive",
        )




    def nav_change(self, e):
        nav_to_page = {
            0: PublicEventsContainer,
            1: MyEventsContainer,
            2: ProfileContainer,
        }
        
        selected_page = nav_to_page.get(e.control.selected_index, ValueError("Invalid index"))(self.page)

        self.appbar.title = ft.Text(selected_page.name)
        self.controls = [selected_page.content]
        self.update()