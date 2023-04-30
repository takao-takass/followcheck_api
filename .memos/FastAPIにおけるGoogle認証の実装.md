## Question
Fast APIを使って、PythonのWebアプリケーションを開発しています。Googleアカウントによるログインを実装したいです。どのようにセットアップしたらよいですか？

## Answer
GoogleアカウントによるログインをFastAPIを使ってPythonのWebアプリケーションに実装するには、以下の手順に従ってください。

1. Google API Consoleでプロジェクトを作成:
まず、Google API Console (https://console.developers.google.com/) にアクセスして、新しいプロジェクトを作成します。プロジェクトを作成したら、左側のナビゲーションメニューから「認証情報」を選択し、「OAuth同意画面」タブに移動して、アプリケーションの詳細を入力します。

2. OAuthクライアントIDを作成:
「認証情報」タブで「認証情報を作成」ボタンをクリックし、「OAuthクライアントID」を選択します。アプリケーションの種類を「ウェブアプリケーション」にし、適切なリダイレクトURIを設定してください。これにより、クライアントIDとクライアントシークレットが生成されます。これらの値は後で必要になります。

3. 必要なライブラリをインストール:
FastAPIを使用するには、以下のライブラリが必要です。

- fastapi
- uvicorn
- python-multipart
- python-jose
- google-auth
- google-auth-oauthlib

これらをインストールするには、次のコマンドを実行します。

``` bash
pip install fastapi uvicorn python-multipart python-jose google-auth google-auth-oauthlib
```

4. 以下のコードは、Googleアカウントを使ってログインする機能を持つFastAPIアプリケーションを作成する方法を示しています。2番目の手順で取得した`CLIENT_ID`と`CLIENT_SECRET`を使用してください。

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from pydantic import BaseModel

app = FastAPI()

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "your-redirect-uri"
SCOPES = ["openid", "email", "profile"]

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://accounts.google.com/o/oauth2/token",
    refreshUrl="https://accounts.google.com/o/oauth2/token",
    clientId=CLIENT_ID,
    clientSecret=CLIENT_SECRET,
    scopes=SCOPES,
)

@app.get("/login")
async def login():
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, _ = flow.authorization_url(prompt="consent")

    return {"url": authorization_url}

class Token(BaseModel):
    code: str

@app.post("/callback")
async def callback(token: Token):
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI

    try:
        flow.fetch_token(code=token.code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch token."
        )

    credentials = Credentials.from_authorized_user_info(info=flow.credentials.to_json())
    email = credentials.id_token.get("email")
    name = credentials.id_token.get("name")
    picture = credentials.id_token.get("picture")

    # ここでユーザー情報をデータベースに保存し、セッションを開始するなど、
    # アプリケーション固有の処理を実行できます。

    return {"email": email, "name": name, "picture": picture}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
```

まず、/loginエンドポイントにアクセスすると、Googleアカウントでの認証を求めるページにリダイレクトされます。認証が成功すると、/callbackエンドポイントにリダイレクトされ、アクセストークンが取得されます。最後に、ユーザーのプロフィール情報（メールアドレス、名前、プロフィール画像）が返されます。

この例では、ユーザー情報をデータベースに保存したり、セッションを開始したりする処理は省略しています。これらの処理は、アプリケーションの要件に応じて実装してください。

## Question
その後のWeb APIアクセスにおいて、Googleアカウントのアクセストークンは、どのように認証に使用すればよいですか？

## Answer
Googleアカウントのアクセストークンを使用してWeb APIへのアクセスを認証するには、FastAPIの`Depends`機能と`OAuth2PasswordBearer`を利用して認証を実装します。以下に、基本的な例を示します。

1. 必要なライブラリをインポート:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests
```

2. `OAuth2PasswordBearer`を設定:

```python
CLIENT_ID = "your-client-id"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

3. アクセストークンの検証用関数を作成:

```python
def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if "email" not in idinfo:
            raise ValueError("Email is not present in token")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return idinfo
```

4. 認証が必要なエンドポイントに`Depends`を使用:

```python
@app.get("/protected")
async def protected_route(user=Depends(authenticate_user)):
    return {"message": "This is a protected route!", "user": user}
```

この例では、`authenticate_user`関数を使用してアクセストークンを検証し、認証されたユーザーの情報を取得します。この関数は`Depends`を使って`protected_route`エンドポイントに依存関係として追加されており、エンドポイントへのアクセスが認証されていることを確認します。認証が成功した場合、`user`には認証済みユーザーの情報が格納され、エンドポイントの処理が続行されます。

この例では、アクセストークンはヘッダーの`Authorization`フィールドに`Bearer`スキームを使用して送信されることを想定しています。アクセストークンが無効または不足している場合、エンドポイントは`401 Unauthorized`ステータスコードを返します。