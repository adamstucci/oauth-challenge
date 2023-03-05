from flask import Flask, request, redirect
import secrets
import requests

app = Flask(__name__)

client_id = "1081824087879462922"
client_secret = "1NK66VevaQQoXQp0y__jd_DNbLtcSqim"

users = {}

app.secret_key = "averysecurepassword"

def exchange_code(code):
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': "http://localhost:5000/"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
#   r.raise_for_status()
  return r.json()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        # return "Hello, Flask!"
        if "code" in request.args:
            code_json = exchange_code(request.args["code"])
            print(code_json)
            discord_response = requests.get("https://discord.com/api/v10/users/@me", headers={"Authorization" : f"{code_json['token_type']} {code_json['access_token']}",
                                                                                              "User-Agent": "scrub2maddog-bootcamp (http://localhost:5000/, 1)"})
            print(discord_response.request.method)
            print(discord_response.request.headers)
            response_json = discord_response.json()
            print(response_json)
            return f"hello {response_json['username']}"

        else: return '<form action="" method="post"><button name="login-btn" value="login">Log in with discord</button></form>'
    
    if request.method == "POST":
        state = secrets.randbits(128)
        redir = redirect("https://discord.com/api/oauth2/authorize?client_id=1081824087879462922&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&response_type=code&scope=identify")
        # print(redir.headers)
        return redir

if __name__ == "__main__":
    app.run(debug=True)