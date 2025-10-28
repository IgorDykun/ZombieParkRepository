from locust import HttpUser, task, between

class ZombieParkUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def view_home(self):
        """Користувач заходить на головну сторінку"""
        self.client.get("/")

    @task(1)
    def view_login(self):
        """Користувач відкриває сторінку входу"""
        self.client.get("/login")

    @task(1)
    def view_register(self):
        """Користувач відкриває сторінку реєстрації"""
        self.client.get("/register")
