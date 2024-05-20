from wallet import Client, Wallet


if __name__ == '__main__':
    c = Client(profile='main', headless=True)

    # To send coins within a telegram, you need to receive an “auth_token”
    # from Wallet directly in chat with the recipient

    auth_token = c.get_token(username='username_to_recieve')
    print(c.receiver_id)  # browser parse tg_id by username

    w = Wallet(auth_token, log_response=True)
    w.send_to_user(amount=1, currency='USDT', receiver_tg_id=c.receiver_id)
