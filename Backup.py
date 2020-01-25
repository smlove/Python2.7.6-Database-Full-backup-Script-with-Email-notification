import mysql.connector
import os
import time
import datetime
import pipes
import smtplib, ssl
import logging

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "senderemail@gmail.com"
receiver_email = "receiveremail@gmail.com"
password = 'enterpassword'

logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(levelname)s %(lineno)d %(message)s', 
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG) 

x = str(mysql_user)
y = str(mysql_password)


user = x.strip()
passwd = y.strip()
logger.info("The Login Detail has been Entered") 

BACKUP_PATH = "/backup/path/enter/here"
logger.info("This is the pass from BACKUP_PATH")

DATETIME = time.strftime('%Y%m%d-%H%M%S')
now = datetime.datetime.now()
logger.info("This is the function for creating date and time of now")

TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
try:
    os.stat(TODAYBACKUPPATH)
    logger.error("Backup path not available")

except:
    os.mkdir(TODAYBACKUPPATH)
    logger.info("A new Backup Path has been Created")

try:
    logger.info("start databsee connection")
    mydb = mysql.connector.connect(
    user=user,
    password=passwd)
    mycursor = mydb.cursor()
    logger.info("MySql Connected to the database")
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        db = x[0]
        print("The Database name: ", db)
        dumpcmd = "mysqldump -u " + " " + user + " -p" + passwd + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        message = """
        Subject: Backup Done

        The Database Backup has been done Successfully ."""
    print("Please Check you Email account Regarding to The Backup") 
        
except Exception as e:
    print(e)
    logger.info("Login Detail Entered By you may be wrong")
    message = """
        Subject: Backup Not Done

        The Database Backup has been not done ."""

#context = ssl.create_default_context()
server = smtplib.SMTP_SSL(smtp_server)
#server.ehlo()
#server.starttls()
#server.ehlo()
server.login(sender_email, password)
logger.info("Gmail login done")
server.sendmail(sender_email, receiver_email, message)
logger.info("Email has been sent")
server.quit()
