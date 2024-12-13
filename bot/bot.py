# ./VK-Vigil/bot/bot.py

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from loguru import logger
from vk_api import VkApi

from config import configs


class Bot:
    def __init__(self, acces_token: str, api_version: str) -> None:
        session = VkApi(
            token=acces_token,
            api_version=api_version,
        )
        self.api = session.get_api()

    def _get_callback_handler(self):
        CallbackHandler.api = self.api
        return CallbackHandler

    def run(self, port=8080):
        server_address = ("", port)
        httpd = HTTPServer(server_address, self._get_callback_handler())

        logger.info(f"Starting server on port {port}...")
        httpd.serve_forever()


class CallbackHandler(BaseHTTPRequestHandler):
    api: Any

    # overriding for disable default logging
    # TODO: In the future, figure out how to redirect the output of logs
    def log_message(self, formant, *args): ...

    def do_POST(self):
        if self.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data)

        # Проверяем подлинность запроса
        if not self._verify_request(payload):
            self.send_response(403)
            self.end_headers()
            return

        if payload.get("type") == "confirmation":
            logger.info("Server confirmation request has been received.")
            self._send_confirmation_response()
        else:
            self._handle_event(payload)

    def _verify_request(self, payload):
        if "secret" not in payload:
            return False

        return payload["secret"] == configs.bot.secret_key

    def _send_confirmation_response(self):
        confirmation_code = self.api.groups.getCallbackConfirmationCode(
            group_id=configs.bot.group_id
        )["code"]

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        logger.debug(
            f"Response has been sent with confirmation code '{confirmation_code}'."
        )
        self.wfile.write(confirmation_code)

    def _handle_event(self, payload):
        logger.debug(payload)

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")
