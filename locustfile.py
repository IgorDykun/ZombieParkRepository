from locust import HttpUser, task, between

class ZombieParkUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_home(self):
        self.client.get("/")

    @task(2)
    def view_register(self):
        self.client.get("/register")

    @task(2)
    def view_login(self):
        self.client.get("/login")

    @task(1)
    def view_tickets(self):
        self.client.get("/tickets")

    @task(1)
    def view_my_tickets(self):
        self.client.get("/my_tickets")

class ZombieParkAdmin(HttpUser):
    wait_time = between(2, 4)

    @task(2)
    def view_admin_home(self):
        self.client.get("/admin_home")

    @task(2)
    def view_admin_tickets(self):
        self.client.get("/admin/tickets")
