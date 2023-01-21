import mysql.connector

connection=mysql.connector.connect(
     host="YOUR HOST",
     user="YOUR USERNAME",
     password="YOUR PASSWORD",
     database="YOUR DATABASE",
)
cursor=connection.cursor()

guild_id="YOUR GUILD ID"
token="YOUR TOKEN"
prefix_bot="!"
