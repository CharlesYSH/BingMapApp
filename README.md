
## 在你開始之前

確保您具有以下內容：
- 一個 [Heroku](https://www.heroku.com) 的帳戶（您可以免費創建一個）

## 架設範例網站

按照以下步驟架設一個網站。


1. 登入 Heroku 後，
  在 [Heroku](https://dashboard.heroku.com/apps) 頁面中，點選 New -> Create New App
  ![](https://i.imgur.com/Y3njp7I.png)
2. 輸入自己喜歡的 App name ，然後點擊 Create app
  ![](https://i.imgur.com/WJ85jXR.png)
3. 下載 [範例程式碼](https://github.com/yaoandy107/line-bot-tutorial/archive/master.zip)

5. 取得 **channel secret** 和 **channel access token**，如果沒有內容，請點 Issue
  ![](https://i.imgur.com/entIggx.png)
6. 使用編輯器開啟範例程式碼資料夾內的 app.py，填入 **channel secret** 和 **channel access token**
  ![](https://i.imgur.com/Uz16joi.png)
7. 並使用 Heroku CLI 將程式部署到 Heroku 上面 （請參考 [使用 Heroku CLI](#使用-heroku-cli)）
8. 使用以下 URL 格式在控制台中輸入 webhook URL 
  `{HEROKU_APP_NAME}.herokuapp.com/callback`
  注意：{HEROKU_APP_NAME} 是步驟2中的應用程序名稱


## 使用 Heroku CLI

1. 下載並安裝 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)、[Git](https://git-scm.com/)
2. 開啟範例程式碼資料夾，在路徑上輸入 cmd
3. 使用終端或命令行應用程序登錄到 Heroku
```shell＝
heroku login
```
4. 初始化 git
``` shell=
$ git config --global user.name "你的名字"
$ git config --global user.email 你的信箱
```
5. 將資料夾初始成 git 空間
```shell＝
git init
```
6. 用 git 將資料夾與 heroku 連接
```shell＝
heroku git:remote -a {HEROKU_APP_NAME}
```
    注意：{HEROKU_APP_NAME} 是上述步驟2中的應用名稱
7. 將資料夾底下所有檔案加入 git 清單，如跳出錯誤訊息請重新執行
```shell
git add .
```
8. 儲存記錄點，如跳出錯誤訊息請詳讀
```shell
git commit -m "Init"
```
    注意："Init" 可使用任意文字替換，其為此紀錄點的敘述
9. 將在 git 清單中的檔案上傳到 heroku，請確認訊息是否顯示成功
```shell
git push heroku master
```
**每當需要更新 Bot 時，請重新執行 7、8、9 步驟**

第一次操作完請回到 [架設範例機器人](#架設範例機器人) 第 5 項繼續接下來的步驟
## 檢查你的日誌
```
當成是遇到問題時，可查看日誌以找出錯誤
```
要查看您的機器人在 Heroku 的日誌，請按照以下步驟。

1. 如果沒登入，請先透過 Heroku CLI 登入
```shell
heroku login
```

2. 顯示 app 日誌
```shell
heroku logs --tail --app {HEROKU_APP_NAME}
```
注意：{HEROKU_APP_NAME} 是上述步驟2中的應用名稱。
​    
    --tail    # 持續打印日誌
    --app {HEROKU_APP_NAME}    # 指定 App

## 程式解說
```
資料夾裡需含有兩份文件來讓你的程式能在 heroku 上運行
```
- Procfile：heroku 執行命令，web: {語言} {檔案}，這邊語言為 python，要自動執行的檔案為 app.py，因此我們改成 **web: python app.py**。
- requirements.txt：列出所有用到的套件，heroku 會依據這份文件來安裝需要套件

