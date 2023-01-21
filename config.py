import mysql.connector

connection=mysql.connector.connect(
     host="YOUR HOST",
     user="YOUR USERNAME",
     password="YOUR PASSWORD",
     database="YOUR DATABASE",
)
cursor=connection.cursor()

token="YOUR TOKEN"
prefix_bot="!"