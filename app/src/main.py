import flet as ft
import logging

from pages import StartView, CreateEventView, InspectEventView

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

def main(page: ft.Page):
    # routing function
    def route_change(e: ft.RouteChangeEvent):
        if "/event/" in e.route:
            event_id = int(e.route.split("/")[-1])
            page.views.append(InspectEventView(page, event_id))

        elif e.route == "/":
            page.views.pop()
            page.views.clear()
            page.views.append(StartView(page))

        else:
            route_to_view = {
                "/create": CreateEventView(page),
            }

            selected_view = route_to_view.get(e.route, ValueError("Route not found"))
            page.views.append(selected_view)
        page.update()

    # set current user
    page.session.set("user_id", 1)

    # set start page
    page.on_route_change = route_change
    page.views.append(StartView(page))

    page.update()



if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")