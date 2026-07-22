from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Jeda acak antar request dari tiap user (0.1 - 0.5 detik)
    wait_time = between(0.1, 0.5)

    @task
    def test_get_products(self):
        # Menembak endpoint catalog/products
        self.client.get("/products/")