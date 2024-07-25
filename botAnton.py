import asyncio
from nio import AsyncClient, MatrixRoom, RoomMessageText, LoginResponse
import subprocess
import os
import sys
import json

class MatrixBot:
    def __init__(self, homeserver, user_id, password):
        self.client = AsyncClient(homeserver, user_id)
        self.password = password
        self.since_token = None

    async def login(self):
        response = await self.client.login(password=self.password)
        if isinstance(response, LoginResponse):
            print("Logged in successfully!")
        else:
            print(f"Failed to log in: {response}")
            return False
        return True

    def is_valid_date_format(self, date_string):
        try:
            day, month, year = map(int, date_string.split('.'))
            return True
        except ValueError:
            return False

    def parse_command(self, message):
        command_prefix = "!отчет"
        if message.startswith(command_prefix):
            date_range = message[len(command_prefix):].strip()
            dates = date_range.split(" - ")
            if len(dates) == 2 and all(self.is_valid_date_format(date) for date in dates):
                return date_range
        return None

    async def message_callback(self, room: MatrixRoom, event: RoomMessageText):
        date_range = self.parse_command(event.body)
        if date_range:
            # Отправка сообщения "Сейчас будет"
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": "Сейчас будет"}
            )

            # Запуск внешнего Python-скрипта с аргументом
            print(f"Running script with date range: {date_range}")
            subprocess.run(["python3", "/home/daniel/projekts/Python/uzkh/GetReport.py", date_range])

            directory_path = "/home/daniel/projekts/Python/uzkh/files/"
            file_name = max(
                (f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))),
                key=lambda x: os.path.getctime(os.path.join(directory_path, x))
            )
            file_path = os.path.join(directory_path, file_name)
            print(f"Checking if file exists at: {file_path}")

            if os.path.exists(file_path):
                print(f"File found: {file_path}. Uploading...")
                # Загрузка файла в Matrix
                with open(file_path, "rb") as file:
                    response, _ = await self.client.upload(
                        file,
                        content_type="application/vnd.ms-excel",
                        filename=file_name
                    )

                # Десериализация и проверка ответа
                response_text = await response.transport_response.text()
                response_json = json.loads(response_text)
                print(f"Upload response JSON: {response_json}")

                if 'content_uri' in response_json:
                    content_uri = response_json['content_uri']
                    print(f"File uploaded successfully: {content_uri}")
                    # Отправка файла в чат
                    await self.client.room_send(
                        room_id=room.room_id,
                        message_type="m.room.message",
                        content={
                            "msgtype": "m.file",
                            "body": file_name,
                            "url": content_uri
                        }
                    )
                    # Удаление файла после успешной отправки
                    os.remove(file_path)
                    print(f"File {file_path} deleted successfully.")
                else:
                    print("Upload failed, content_uri is missing.")
                    await self.client.room_send(
                        room_id=room.room_id,
                        message_type="m.room.message",
                        content={"msgtype": "m.text", "body": "Не удалось загрузить файл."}
                    )
            else:
                print("File not found.")
                await self.client.room_send(
                    room_id=room.room_id,
                    message_type="m.room.message",
                    content={"msgtype": "m.text", "body": "Файл не найден."}
                )

        self.since_token = event.server_timestamp

    async def main(self):
        if not await self.login():
            sys.exit(1)

        # Начальная синхронизация для получения since_token
        response = await self.client.sync()
        self.since_token = response.next_batch

        self.client.add_event_callback(self.message_callback, RoomMessageText)

        await self.client.sync_forever(timeout=30000, since=self.since_token)

if __name__ == "__main__":
    homeserver = ""  # Замените на адрес вашего homeserver
    user_id = ""  # Замените на ваш user_id @bot:matrix.ru
    password = ""  # Замените на ваш пароль

    bot = MatrixBot(homeserver, user_id, password)
    asyncio.run(bot.main())
