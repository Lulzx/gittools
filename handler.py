import web
import json
import oauth2
import requests

urls = ('/', 'githublogin',
        '/githubcallback', 'githubCallback')
render = web.template.render('templates/')


def GET_LOGIN():
    client_id = ''
    url_string = "https://github.com/login/oauth/authorize?client_id=" + client_id
    return render.index(url_string)


def GET_CALLBACK():
    data = json.loads(json.dumps(web.input()))
    print(data['code'])
    headers = {'content-type': 'application/json'}
    pay_load = {'client_id': '',
                'client_secret': '',
                'code': data['code']}
    r = requests.post('https://github.com/login/oauth/access_token', data=json.dumps(pay_load), headers=headers)
    token_temp = r.text.split('&')
    token = token_temp[0].split('=')
    access_token = token[1]
    repo_url = 'https://api.github.com/user?access_token=' + access_token
    response = requests.get(repo_url)
    final_data = response.content
    print(final_data)


app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
