import time

from wallet import Client


def token_to_file():
    while True:
        try:
            client = Client(profile='main')
            auth_token = client.get_token()

            with open('token.txt', 'w') as f:
                f.write(auth_token)

            time.sleep(60*5)
            client.stop()
        except Exception as e:
            print(f"[!] Error update_token: {e}")
            time.sleep(15)


if __name__ == '__main__':
    token_to_file()
