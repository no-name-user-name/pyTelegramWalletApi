import time

from wallet import Client


def token_to_file():
    while True:
        try:
            client = Client(profile='main', headless=False)

            try:
                auth_token = client.get_token()
                print(auth_token)
                with open('token.txt', 'w') as f:
                    f.write(auth_token)
            except Exception as e:
                raise Exception(f"[!] Error get_token: {e}")
            finally:
                client.stop()

            time.sleep(60*5)
        except Exception as e:
            print(f"[!] Error update_token: {e}")
            time.sleep(15)


if __name__ == '__main__':
    token_to_file()
