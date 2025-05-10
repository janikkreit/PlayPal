import flet as ft

from database import Database, User

class ProfileContainer(ft.Container):
    def __init__(self, page: ft.Page):
        def save_click(e):
            # check if text fields are empty
            if not self.username.value:
                return
        
            db = Database("events-users")
            
            try:
                db.add_user(User(username=self.username.value))
                page.open(ft.SnackBar(ft.Text("Username saved successfully")))
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    page.open(ft.SnackBar(ft.Text("Changed to user")))
                else:
                    print(e)

            user_id = db.get_user_by_username(self.username.value).id
            page.session.set("user_id", user_id)


        self.name = "Profile"
        self.page = page

        db = Database("events-users")

        user = db.get_user_by_id(page.session.get("user_id"))
        if user is not None:
            username = user.username
        else:
            username = ""
        self.username = ft.TextField(username, label="Username", autofocus=True)

        super().__init__(
            content=ft.Column(
                [
                    self.username,
                    ft.ElevatedButton("Save", on_click=save_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )
