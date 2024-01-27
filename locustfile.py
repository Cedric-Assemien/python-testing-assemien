from locust import HttpUser,task

class test_de_route(HttpUser):
    @task
    def test_route(self):
        self.client.get('/')
        self.client.get('/showSummary')
        self.client.get('/purchasePlaces')
        self.client.get('/logout')
        self.client.get('/book/<competition>/<club>')