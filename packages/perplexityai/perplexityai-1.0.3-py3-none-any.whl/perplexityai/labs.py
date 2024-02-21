from uuid import uuid4
from requests import Session
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp


class Labs:
    def __init__(self):
        self.history = []
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false",
                "X-Client-Name": "Perplexity-iOS",
            }
        )
        self._init_session_without_login()

        self.t = format(getrandbits(32), "08x")
        self.sid = loads(
            self.session.get(
                url="https://labs-api.perplexity.ai/socket.io/?transport=polling&EIO=4"
            ).text[1:]
        )["sid"]

        self.queue = []
        self.finished = True

        assert self._ask_anonymous_user(), "failed to ask anonymous user"
        self.ws = WebSocketApp(
            url=f"wss://labs-api.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header=self._get_headers(),
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=lambda ws, err: print(f"websocket error: {err}"),
        )
        Thread(target=self.ws.run_forever).start()
        self._auth_session()

        while not (self.ws.sock and self.ws.sock.connected):
            import time

            time.sleep(0.01)

    def _init_session_without_login(self):
        self.session.get(url=f"https://www.perplexity.ai/search/{str(uuid4())}")
        self.session.headers.update(
            {"User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false"}
        )

    def _auth_session(self):
        self.session.get(url="https://www.perplexity.ai/api/auth/session")

    def _ask_anonymous_user(self):
        response = self.session.post(
            url=f"https://labs-api.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
            data='40{"jwt":"anonymous-ask-user"}',
        ).text
        return response == "OK"

    def _get_cookies_str(self):
        return "; ".join(
            [f"{key}={value}" for key, value in self.session.cookies.get_dict().items()]
        )

    def _get_headers(self):
        headers = {"User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false"}
        headers["Cookie"] = self._get_cookies_str()
        return headers

    def _on_open(self, ws):
        ws.send("2probe")
        ws.send("5")

    def _on_message(self, ws, message):
        if message == "2":
            ws.send("3")
        elif message.startswith("42"):
            message = loads(message[2:])[1]
            if "status" not in message:
                self.queue.append(message)
            elif message["status"] == "completed":
                self.finished = True
                self.history.append(
                    {"role": "assistant", "content": message["output"], "priority": 0}
                )
            elif message["status"] == "failed":
                self.finished = True

    def generate_answer(self, prompt, model="mistral-7b-instruct"):
        assert self.finished, "already searching"
        assert model in [
            "mixtral-8x7b-instruct",
            "llava-7b-chat",
            "llama-2-70b-chat",
            "codellama-34b-instruct",
            "mistral-7b-instruct",
            "pplx-7b-chat",
            "pplx-70b-chat",
            "pplx-7b-online",
            "pplx-70b-online",
        ]
        self.finished = False
        self.history.append({"role": "user", "content": prompt, "priority": 0})
        self.ws.send(
            f'42["perplexity_labs",{{"version":"2.2","source":"default","model":"{model}","messages":{dumps(self.history)}}}]'
        )

        while (not self.finished) or (len(self.queue) != 0):
            if len(self.queue) > 0:
                yield self.queue.pop(0)
        self.ws.close()
