# locustfile.py
from locust import User, task, between
import websocket
import threading
import time

class WebSocketUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        # URL do seu servidor WebSocket
        self.ws_url = "wss://6777dd2b-e54b-4947-99d8-4314d35db7d5-00-2yl3goq7svb3l.spock.replit.dev/ws"
        self.ws = None
        self.ws_thread = None
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        time.sleep(1)  # Aguarde a conexão ser estabelecida

    def on_open(self, ws):
        print("Conexão estabelecida")

    def on_message(self, ws, message):
        # Opcional: Processar mensagens recebidas
        pass

    def on_error(self, ws, error):
        print(f"Erro no WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Conexão WebSocket fechada")

    @task
    def send_message(self):
        if self.ws:
            start_time = time.time()
            try:
                self.ws.send("Mensagem de teste")
                total_time = (time.time() - start_time) * 1000  # em milissegundos
                # Reporta sucesso para o Locust
                self.environment.events.request.fire(
                    request_type="WebSocket",
                    name="send_message",
                    response_time=total_time,
                    response_length=0,
                    exception=None,
                )
            except Exception as e:
                total_time = (time.time() - start_time) * 1000
                # Reporta falha para o Locust
                self.environment.events.request.fire(
                    request_type="WebSocket",
                    name="send_message",
                    response_time=total_time,
                    response_length=0,
                    exception=e,
                )

    def on_stop(self):
        if self.ws:
            self.ws.close()
