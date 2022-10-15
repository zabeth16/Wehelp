
from flask import Flask , session , redirect , url_for , render_template , request
app = Flask(
    __name__ ,    # __name__ 代表目前執行的模組 這是python內建的變數模式
    static_folder = "static" , # 靜態檔案的資料夾名稱，要改名也可以，不過資料夾名也要記得更動
    static_url_path = "/mysource" # 靜態檔案對應的網址路徑
            ) 
# 所有在 static的檔案名稱都對應在網址路徑，會是 /mysource/檔案名稱 打在網址尾巴

# 首頁區
@app.route("/", methods=["POST","GET"]) # 小老鼠是函式的裝飾(decorator) : 以函式為基礎，附加的功能
def home():
    return render_template("home.html") # 這會呈現在首頁畫面上!


# 驗證功能網址，純驗證用不顯示
@app.route("/signin" , methods = ["POST"])
def signin():
    if request.method == "POST" :
        if (request.form["account"] == "test") and (request.form["psword"] == "test"):
            session["status"] = "已登入"
            return redirect("/member")
        elif (request.form["account"] == "") or (request.form["psword"] == ""):
            session["status"] = "登入失敗"
            return redirect(url_for("error" ,  message ='有帳號或密碼沒輸喔!')) 
        else:
            session["status"] = "登入失敗"
            return redirect(url_for("error" ,  message ='打錯了，請重新輸入帳號密碼!'))



# 成功頁面網址區
@app.route("/member") 
def member():  
    user = session["status"]
    if user == "已登入":
        return render_template("memberSS.html")
        # 記得要防這裡使用者偷吃步，要用資料庫使用者是否登入的狀態去做判斷Session
    else:
        return redirect("/")

# 登入後登出頁面網址區
@app.route("/logout")
def logout():
    session["status"] = "未登入"
    return redirect("/")




# 錯誤頁面網址區
# 這裡固定只能是 GET 方法
@app.route("/error") 
def error():
    if url_for("error" ,  message ='有帳號或密碼沒輸喔!') :
        return render_template("error.html" , message ='有帳號或密碼沒輸喔!')
    else:
        return render_template("error.html" ,  message ='打錯了，請重新輸入帳號密碼!')

    # 原本超級繞的邏輯:
    # if request.args.get("message","") == "有帳號或密碼沒輸喔!" :    
    #     err_empty = request.args.get("message","有帳號或密碼沒輸喔!")
    #     return render_template("error.html" , message = err_empty )
    # else:
    #     err_message =  request.args.get("message","打錯了，請重新輸入帳號密碼")
    #     return render_template("error.html" ,  message = err_message)  



# 建立一個密鑰，內容可以隨便打
app.secret_key = "anyway, that is a secrect"



if __name__ == "__main__": # 如果以主程式執行
    app.run(port=3000 , debug = True) # 啟動伺服器

# import sys
# print("User Current Version:-", sys.version) # 看我Python version 得知是3.10.7




# # 我的專屬錯誤頁提醒，沒有繼續研究下去
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init("測試勇者迷路了嗎?我看你是迷路了喔!", integrations=[FlaskIntegration()])



# 測試理清觀念程式碼區 

# # Query String 
# # 利用要求字串提供彈性 /getSum?max=最大數字
# # 求 1+2+3往上疊加，至一個max值，max值由前端給
# @app.route("/getSum") 
# def getSum(): # 1+2+3+...+max 是彈性的
#     maxNumber = request.args.get("max",100) #100是預設max=後方沒寫就是100
#     maxNumber = int(maxNumber)
#     print("最大數字:", maxNumber)
#     result = 0
#     for n in range(1, maxNumber+1 ):
#         result += n        
#     return "結果" + str(result)

# # Query String 
# # 練習並偷試作第四題，求平方，先不要好了QQ
# # 利用要求字串提供彈性 /getSum?max=最大數字
# # 求 1+2+3往上疊加，至一個max值，max值由前端給
# # 新增最小值&最大值都需要
# @app.route("/getSum") 
# def getSum(): # 1+2+3+...+max 是彈性的
#     maxNumber = request.args.get("max",100) #100是預設max=後方沒寫就是100
#     maxNumber = int(maxNumber)
#     print("最大數字:", maxNumber)
#     minNumber = request.args.get("min",1)
#     minNumber = int(minNumber)
#     print("最小數字:", minNumber)
#     result = 0
#     for n in range(minNumber , maxNumber + 1 ):
#         result += n        
#     return "結果" + str(result)


# # 測試用request寫登入後畫面
# # 處理路徑 /show 的對應函式
# @app.route("/show")
# def show():
#     name = request.args.get("account","")
#     return  "歡迎" + name
# # 可以去看看，樣板()裡面是能放參數 = 彈性結果的
# # ("我要導去的頁面.html" , data = str(result))) 數字會直接被變成字串



# # 練習session 區
# # 利用 GET 方法處理路徑 /hello?name=使用者打的名字
# @app.route("/hello")
# def hello():
#     user = request.args.get("name" , "")
#     session["record_name"] = user
#     return "安安，" + user

# # 利用 GET 方法處理路徑
# @app.route("/talk")
# def talk():
#     user = session["record_name"]
#     return user + "今天很嗆是吧!"