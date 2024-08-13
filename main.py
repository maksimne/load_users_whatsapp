import requests
import json
import time
from flask import *

app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
MAX_FILE_SIZE = 1024 * 1024 * 1024
list_num = []

def add_users(group_id, numbers, wa_instance, api_token_instance):
    for num in numbers:
        url = "https://7103.api.greenapi.com/waInstance" + str(wa_instance) + "/addGroupParticipant/" + str(api_token_instance)

        payload = "{\r\n\t\"groupId\": \"" + str(group_id) + "@g.us\",\r\n\t\"participantChatId\": \"" + str(num) + "@c.us\"\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }
        time.sleep(1)

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))
        print(num)



@app.route('/')
def main():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == "POST":
        file = request.files["file"]

        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            file_info = json.loads(file_bytes.decode())
            for i in file_info['numbers']:
                list_num.append(i)
            add_users(group_id=file_info['groupId'], numbers=list_num, wa_instance=file_info['waInstance'],
                      api_token_instance=file_info["apiTokenInstance"])
        return render_template("test.html", name=file.filename)


if __name__ == '__main__':
    app.run(debug=True)


