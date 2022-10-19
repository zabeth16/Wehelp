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






