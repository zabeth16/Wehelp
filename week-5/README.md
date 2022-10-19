# WEEK-5 MySQL 練習與展示截圖

## 要求三：SQL CRUD

* 使⽤ INSERT 指令新增⼀筆資料到 member 資料表中，這筆資料的 username 和 password 欄位必須是 test。  
接著繼續新增⾄少 4 筆隨意的資料。  
(這邊因為在創建table與insert data的時候沒截到圖，直接打出程式碼示意)  

先創建資料表:
```MySQL
create table member(  
id bigint primary key auto_increment,  
name varchar(255) not null,  
password varchar(255) not null,  
follower_count int unsigned not null default 0,  
time datetime not null default current_timestamp);
```

insert 資料，以第一筆test為例:  
(故意不輸入follower_count 與 time，測試看看預設是否有效)
```MySQL
insert into member(  
name , username , password)  
values
('測試員' , 'test' , 'test');
```

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料。


![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/03_0102%20select%20all%20from%20member.png?raw=true "03_0102")

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料，  
並按照 time 欄位，由近到遠排序。

![image](https://user-images.githubusercontent.com/40664034/196613081-8d6e52bb-1311-4675-9180-10d431ce932b.png)

* 使⽤ SELECT 指令取得 member 資料表中第 2 ~ 4 共三筆資料，並按照 time 欄位，  
由近到遠排序。( 並非編號 2、3、4 的資料，⽽是排序後的第 2 ~ 4 筆資料 )
![image](https://user-images.githubusercontent.com/40664034/196613344-4aba9adf-1d41-47d3-ab29-26999b28680c.png)

* 使⽤ SELECT 指令取得欄位 username 是 test 的會員資料。
![image](https://user-images.githubusercontent.com/40664034/196613676-c3f0fd04-b027-4d72-8d9d-29d1b1bcb4a8.png)

* 使⽤ SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。
![image](https://user-images.githubusercontent.com/40664034/196613763-fbd59d4c-b2bf-49a0-8555-e11832b585d2.png)

* 使⽤ UPDATE 指令更新欄位 username 是 test 的會員資料，  
將資料中的 name 欄位改成 test2。  
附上原本table做對照。
![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/03_07%20update.png?raw=true "03_07 update")


## 要求四：SQL Aggregate Functions

* 取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。 
![image](https://user-images.githubusercontent.com/40664034/196614739-ed614aea-08c8-416c-aacd-ca75aa1970cc.png)

* 取得 member 資料表中，所有會員 follower_count 欄位的總和。
![image](https://user-images.githubusercontent.com/40664034/196614782-b6d3fb56-127a-43a7-bc7d-8bd60675bb25.png)

* 取得 member 資料表中，所有會員 follower_count 欄位的平均數。
![image](https://user-images.githubusercontent.com/40664034/196614819-4d73387b-65b0-4890-9f8c-762e79bace33.png)

## 要求五：SQL JOIN (Optional)
* 使⽤ SELECT 搭配 JOIN 語法，取得所有留⾔，結果須包含留⾔者會員的姓名。
(附上原 table messaege 作對照)
![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/05_01%20join.png?raw=true "05_01 join")

* 使⽤ SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔，資料中須包含留⾔者會員的姓名。
![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/05_02%20join%20where.png?raw=true "05_02 join where")

* 使⽤ SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔平均按讚數。
![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/05_03%20join%20avg%20where.png?raw=true "05_03 join avg")


## 其他: 匯出指定資料庫 mysqldump
![github](https://github.com/zabeth16/Wehelp/blob/main/week-5/ScreenShot/06%20final%20output.png?raw=true "output")

# 以上，感謝閱讀 ! BY ZABETH
