# followcheck_api

- AIが1時間で作ってくれました。
- followcheckのデータベースを使っています。

# 手順
1. このリポジトリをクローンする
1. venvを作成します。
    ``` bash
    python -m venv <your_venv_nanme>
    ```
1. 依存関係をインストールします。
    ``` bash
    pip install -r requirements.txt
    ```
1. config.jsonをトレースしないように設定します。
    ``` bash
    git update-index --skip-worktree config.json
    ```
