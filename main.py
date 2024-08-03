from flask import Flask, request, render_template, redirect, url_for

import requests

import time

import threading

app = Flask(__name__)

headers = {

    'Connection': 'keep-alive',

    'Cache-Control': 'max-age=0',

    'Upgrade-Insecure-Requests': '1',

    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

    'Accept-Encoding': 'gzip, deflate',

    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',

    'referer': 'www.google.com'

}

@app.route('/', methods=['GET', 'POST'])

def send_message():

    if request.method == 'POST':

        tokens = [token.strip() for token in request.form.get('tokens').split('\n')]

        convo_id = request.form.get('convo_id').strip()

        messages = [msg.strip() for msg in request.form.get('messages').split('\n')]

        haters_name = request.form.get('haters_name').strip()

        speed = int(request.form.get('speed'))

        num_messages = len(messages)

        num_tokens = len(tokens)

        post_url = "https://graph.facebook.com/v13.0/{}/".format('t_' + convo_id)

        while True:

            try:

                for message_index in range(num_messages):

                    token_index = message_index % num_tokens

                    access_token = tokens[token_index]

                    message = messages[message_index]

                    parameters = {'access_token': access_token,

                                  'message': haters_name + ' ' + message}

                    response = requests.post(post_url, json=parameters, headers=headers)

                    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                    if response.ok:

                        print(f"\033[1;32;1m[Ã¢Å“â€œ]SEND SUCCESSFUL No. {message_index + 1}")

                        print(f"\033[1;32;1m[+]Thread ID: {threading.get_ident()}")

                        print(f"\033[1;32;1m[+]Token No.{token_index + 1}")

                        print(f"\033[1;32;1m[+]Message: {haters_name} {message}")

                        print(f"\033[1;32;1m[+]Time: {current_time}")

                        print("\n" * 2)

                    else:

                        print(f"\033[1;31;1m[x]Failed to send Comment No. {message_index + 1}")

                        print(f"\033[1;31;1m[+]Thread ID: {threading.get_ident()}")

                        print(f"\033[1;31;1m[+]Token No.{token_index + 1}")

                        print(f"\033[1;31;1m[+]Message: {haters_name} {message}")

                        print(f"\033[1;31;1m[+]Time: {current_time}")

                        print("\n" * 2)

                    time.sleep(speed)

            except Exception as e:

                print(e)

                time.sleep(30)

    return render_template('index.html')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
