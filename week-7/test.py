import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="zabeth16",
  database="farm",
)

# print(mydb)

mycursor = mydb.cursor()

# 我新資料庫就是小雞農場，farm
#mycursor.execute("CREATE DATABASE farm")

# 先創建一個table 也是叫 member
# 使用者名字: name、帳號: account (有改成username)、密碼: password
# 先不考慮 content 的部分
# mycursor.execute("CREATE TABLE member (id BIGINT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL,account VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")

# # 建立另外的table egg做註冊帳號比對
# mycursor.execute("CREATE TABLE egg (id BIGINT AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255) NOT NULL , username VARCHAR(255) , password VARCHAR(255) NOT NULL )")

# # 練習insert資料
# column = "INSERT INTO member (name, account , password) VALUES ('測試一號' , 'test' , 'test')"
# mycursor.execute(column)

# 看看insert 第二、三筆資料
# column = "INSERT INTO member (name, username , password) VALUES (%s, %s, %s)"
# values = ("測試三號" , "test3" , "test3")
# mycursor.execute(column,values)

#必要的 It is required to make the changes, otherwise no changes are made to the table.
mydb.commit()

# # VS terminal 預覽是否有插入資料成功
# print(mycursor.rowcount, "was inserted.")



# mycursor.execute("SELECT name FROM member WHERE username = 'test' ")

# myresult = mycursor.fetchone()

# 看單筆row資料用的
# myresult = mycursor.fetchone()


# 拿來看我新增的資料
# mycursor.lastrowid 我是都顯示0，乾脆拿掉
# print("new record , ID:", myresult[0])

# #這邊是可以用VS terminal看到資料庫的東西，但還是不太習慣
# for x in mycursor:
#   print(x)

mycursor.close()