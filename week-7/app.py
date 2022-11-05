from select import select
from unittest.mock import patch
from flask import Flask , session , redirect , url_for , render_template , request , jsonify , make_response
import requests , json

app = Flask(
    __name__ ,    # __name__ 代表目前執行的模組 這是python內建的變數模式
    static_folder = "static" , # 靜態檔案的資料夾名稱，要改名也可以，不過資料夾名也要記得更動
    static_url_path = "/mysource" # 靜態檔案對應的網址路徑
            ) 
# 所有在 static的檔案名稱都對應在網址路徑，會是 /mysource/檔案名稱 打在網址尾巴


# 將json中文字不要自動轉成亂碼，能顯示中文。
app.config["JSON_AS_ASCII"] = False


# ============================================

# 我的資料庫區 database: farm
# table: member
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="zabeth16",
  database="farm"
)

mycursor = mydb.cursor() # 我的卡車


# ============================================


# 首頁區
@app.route("/", methods=["POST","GET"]) # 小老鼠是函式的裝飾(decorator) : 以函式為基礎，附加的功能
def home():
    return render_template("home.html") # 這會呈現在首頁畫面上!


# ============================================



# 註冊驗證功能網址
@app.route("/signup", methods = ["POST"])
def signup():
    username = request.form["username"]  
    mycursor.execute('SELECT username FROM member WHERE username = %s ', (username,)) # 只有單個參數時username後方逗號是必要的
    checkUsername = mycursor.fetchall()   
 
    # username 有重複的情況
    if len(checkUsername) > 0 :
        session["status"] = "註冊失敗"
        return redirect(url_for("error" ,  message ='註冊帳號有重複，請想其他的!'))

    
    # 註冊任何欄位空白
    elif (request.form["name"] == "") or (request.form["username"] == "") or (request.form["psword_s"] == ""):
        session["status"] = "註冊失敗"
        return redirect(url_for("error" ,  message ='註冊欄位不可空白沒輸喔!')) 

    # username 不重複，來新增進去
    else:
        # 來把form輸入的insert到database table裡面
        name = request.form["name"]
        username = request.form["username"]
        psword = request.form["psword_s"]
        
        mycursor.execute( "INSERT INTO member (name, username , password) VALUES (%s,%s,%s)",(name,username,psword))
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
        session["status"] = "已註冊"
        return redirect(url_for("member" , message = '註冊成功'))
        


# ============================================


# 登入驗證功能網址區，純驗證用不顯示
@app.route("/signin" , methods = ["POST"])
def signin():

    account = request.form["account"]
    psword = request.form["psword"]
    mycursor.execute('SELECT * FROM member WHERE username = %s and password = %s ', (account,psword))
    get_user = mycursor.fetchall()
    session["check"] = get_user

    if len(get_user) > 0 :
        session["status"] = "已登入" 
        mycursor.execute('SELECT * from member WHERE username = %s ', (account,))
        session["record"] = mycursor.fetchall()        
        return redirect("member" )

    elif (request.form["account"] == "") or (request.form["psword"] == ""):
        session["status"] = "登入失敗"
        return redirect(url_for("error" ,  message ='有帳號或密碼沒輸喔!')) 
    else:
        session["status"] = "登入失敗"
        return redirect(url_for("error" ,  message ='打錯或你還沒註冊，請重新輸入帳號密碼!'))



# ============================================


# 成功頁面網址區
@app.route("/member" )
def member(): 
    user = session["status"] 
    # 這邊都是GET，要想想怎麼用session帶過來
    if user == "已登入" :
        name = session["record"]
        print("登入暱稱: " , name[0][1])
      
        i = 0
        mycursor.execute(" SELECT member.name, message.content FROM member INNER JOIN  message ON member.id = message.member_id")
        talk_all = mycursor.fetchall()
        for i in range(len(talk_all)) :

            # print(talk_all[i][0]) # 跑出所有 name FROM message
            # print(talk_all[i][1]) # 跑出所有 content FROM message
            print(talk_all[i][0] , talk_all[i][1] )
        # 看留言長度 
        # print(len(talk_all)) 

        return render_template("memberSS.html"  , all_message = talk_all ,  name = session["record"][0][1]  ,  messageSS = "降落成功，歡迎你!") #純註冊的，但成功登入也會來這        
        
    
    # 註冊成功的
    elif user == "已註冊":        
        return render_template("memberSS.html" , message = "註冊成功"  )

       
    else:
        # 記得要防這裡使用者偷吃步，要用資料庫使用者是否登入的狀態去做判斷Session
        return redirect("/")



# ============================================


# api區，後端整理成json
@app.route("/api/member" , methods = ["GET" , "PATCH"])
def api():
 
    if  request.method == "GET" and session["status"] =="已登入": 
      
        mycursor.execute("SELECT id , name , username FROM member WHERE username = %s" , ( request.args.get("username",""),))
        session["who"] = mycursor.fetchone()
        print(session["who"])

        if session["who"]  != None   :
            print("Succesful connection with API.")
            
            #jsonify
            return  jsonify({"data": 
                        { "id": session["who"][0] ,
                            "name":  session["who"][1] ,
                            "username" :session["who"][2]
                    }})

        else  :
            return jsonify({"data": session["who"] })

    
    elif request.method == "PATCH":
                    
     
        new_name = request.get_json()
        print(new_name["name"])
       
        if new_name["name"] != "" :
            mycursor.execute("UPDATE member SET NAME = %s WHERE id = %s ",(new_name["name"], session["record"][0][0]) )

            return ({ "OK" : True })
        
        else :            
            print("It contains space")
            return ({ "error" : True })

        
    else: 
        return redirect("/")




# ============================================


# 登入後登出頁面網址區
@app.route("/signout")
def logout():
    session["status"] = " "
    session["record"] = " "
    return redirect("/")


# ============================================



# 錯誤頁面網址區
# 這裡固定只能是 GET 方法
@app.route("/error") 
def error():
    # 試著不要執著於判斷式    
    return render_template("error.html" , message = request.args.get("message","")  )



# ============================================

# 留言板區
@app.route("/message" , methods = ["POST"] )
def message():
    # 這邊最好要做已登入session
    talk = request.form["talk"]
    name = session["record"][0][1]
    member_id = session["record"][0][0]
    mycursor.execute( "INSERT INTO message (member_id , content) VALUES (%s , %s)",(member_id , talk))
    mydb.commit()
    print(mycursor.fetchall, "was inserted.")


    return redirect("/member") 

# ============================================


# 建立一個密鑰，內容可以隨便打，session 用
app.secret_key = "anyway, that is a secrect"


# ============================================


if __name__ == "__main__": # 如果以主程式執行
    app.run(port=3000 , debug = True) # 啟動伺服器


# ============================================

# import sys
# print("User Current Version:-", sys.version) # 看我Python version 得知是3.10.7


# ============================================


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
# session[ ] 內可自行命名，記得是用雙引號包起來。



# 紀念html迴圈用
# // function talk(){
    
# //     // for (i = 0 ;  i <= all_message.length ; i++ ){
# //     //     name_message = '{{all_message[0][0] }}'
# //     //     // let label = document.createElement("label");          
# //     //     // div_talking = document.querySelector(".talking");
# //     //     // div_talking.appendChild(label);

# //     //     let talk_box = document.createTextNode(' {{ all_message[0][0] }} '  );
# //     //     label.appendChild(talk_box);
# //     // };
# //     let label = document.createElement("label");          
# //     div_talking = document.querySelector(".talking");
# //     div_talking.appendChild(label);     
# //     let name_box = document.createTextNode(' {{ all_message[0][0] }} 說: {{ all_message[0][1] }}');                
# //     label.appendChild(name_box);

    
# //     // {{ name_message }}  {{ talking }}
# //     // {{ all_message[0][0]  }} {{ all_message[0][1] }}
    
    
# // };


# // talk();