from fastapi import FastAPI, Response, Request
import requests
import webbrowser

app = FastAPI()

client_id = '0oabked9540MRzvA45d7'
okja_num = '87800562'
client_secret = 'j4Dgt8hZtT497GsEOQiuiI6Cql-jrGWsNvsjDWs_CQU0dmvUdjk99Dnj-E6I2x8Z'
string = client_id + client_secret

@app.get("/")
async def root(request : Request):
    if(request.cookies.get('access_token')):
        resp2 = requests.get(f"https://dev-{okja_num}.okta.com/oauth2/default/v1/userinfo",
                    headers={"Authorization" : f"Bearer {request.cookies.get('access_token')}"})
        return resp2.json() 
    return webbrowser.open(f"https://dev-{okja_num}.okta.com/oauth2/default/v1/authorize?scope=openid email profile&response_type=code&state=abcdefgh&client_id={client_id}&redirect_uri=http://localhost:8000/authorization-code/callback/", new=2)
    

@app.get("/authorization-code/callback/")
async def callback(code, response: Response):
    resp = requests.post(f"https://dev-{okja_num}.okta.com/oauth2/default/v1/token",
                            headers={"Content-Type" : 'application/x-www-form-urlencoded'},
                            data={"client_id" : client_id,"client_secret" : client_secret,"grant_type" : 'authorization_code', "code" : code, "redirect_uri" : 'http://localhost:8000/authorization-code/callback/'} )
    resp2 = requests.get(f"https://dev-{okja_num}.okta.com/oauth2/default/v1/userinfo",
                headers={"Authorization" : f'Bearer {resp.json()["access_token"]}'})
    response.set_cookie(key="access_token", value=resp.json()["access_token"], expires=15)
    return resp2.json()