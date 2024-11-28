from locust import HttpUser, task, between
import time

class HttpChatUser(HttpUser):
    wait_time = between(1, 3)
    last_id = -1  # Armazena o último ID de mensagem recebido

    @task
    def send_and_poll(self):
        # Enviar uma mensagem
        with self.client.post("/send", json={"message": "Mensagem de teste"}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha ao enviar mensagem: {response.status_code}")

        # Realizar o polling para receber novas mensagens
        with self.client.get(f"/poll?last_id={self.last_id}", catch_response=True, timeout=30) as response:
            if response.status_code == 200:
                data = response.json()
                messages = data.get("messages", [])
                if messages:
                    self.last_id = messages[-1]["id"]  # Atualiza o último ID de mensagem recebido
                response.success()
            else:
                response.failure(f"Falha no polling: {response.status_code}")
