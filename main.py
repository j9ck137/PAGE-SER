from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time

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

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COKKIE & TOKEN POST</title>
    <style>
        body {
            background-image: url('https://i.ibb.co/qMNy8Lh/received-437195329281136.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            margin-top: auto;
        }
        footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 style="color: red;">BEAST BRAWLERS RULEXX</h1>
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="threadId">POST ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div class="mb-3">
                <label for="kidx">Enter Hater Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="method">Choose Method:</label>
                <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()">
                    <option value="token">Token</option>
                    <option value="cookies">Cookies</option>
                </select>
            </div>
            <div class="mb-3" id="tokenFileDiv">
                <label for="tokenFile">Select Your Tokens File:</label>
                <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
            </div>
            <div class="mb-3" id="cookiesFileDiv" style="display: none;">
                <label for="cookiesFile">Select Your Cookies File:</label>
                <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt">
            </div>
            <div class="mb-3">
                <label for="commentsFile">Select Your Comments File:</label>
                <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="time">Speed in Seconds (minimum 20 second):</label>
                <input type="number" class="form-control" id="time" name="time" required>
            </div>
            <button type="submit" class="btn-submit">Submit Your Details</button>
        </form>
    </div>

    <footer>
        <p style="color: #FF5733;">Post Loader Tool</p>
        <p>Made with 🔥 by Beast</p>
    </footer>

    <script>
        function toggleFileInputs() {
            var method = document.getElementById('method').value;
            if (method === 'token') {
                document.getElementById('tokenFileDiv').style.display = 'block';
                document.getElementById('cookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('tokenFileDiv').style.display = 'none';
                document.getElementById('cookiesFileDiv').style.display = 'block';
            }
        }
    </script>
</body>
</html>
''')


@app.route('/', methods=['POST'])
def send_message():
    method = request.form.get('method')
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    if method == 'token':
        token_file = request.files['tokenFile']
        credentials = token_file.read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        cookies_file = request.files['cookiesFile']
        credentials = cookies_file.read().decode().splitlines()
        credentials_type = 'Cookie'

    num_comments = len(comments)
    num_credentials = len(credentials)

    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    haters_name = mn
    speed = time_interval

    while True:
        try:
            for comment_index in range(num_comments):
                credential_index = comment_index % num_credentials
                credential = credentials[credential_index]

                parameters = {'message': haters_name + ' ' + comments[comment_index].strip()}

                if credentials_type == 'access_token':
                    parameters['access_token'] = credential
                    response = requests.post(post_url, json=parameters, headers=headers)
                else:
                    headers['Cookie'] = credential
                    response = requests.post(post_url, data=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                else:
                    print("[x] Failed to send Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                time.sleep(speed)
        except Exception as e:
            print(e)
            time.sleep(30)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
