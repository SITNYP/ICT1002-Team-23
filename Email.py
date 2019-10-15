import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
globalpath =""
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # check if its an email addr

def check(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(regex, email)):
        return email

    else:
        return False


def reverse_slicing(s):
    return s[::-1]
class Ui_Email(object):

    def setupUi(self, Email):
        Email.setObjectName("Email")
        Email.resize(400, 251)
        self.sendAddr = QtWidgets.QLineEdit(Email)
        self.sendAddr.setGeometry(QtCore.QRect(80, 10, 301, 31))
        self.sendAddr.setInputMask("")
        self.sendAddr.setText("")
        self.sendAddr.setObjectName("sendAddr")
        self.label = QtWidgets.QLabel(Email)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.openFile = QtWidgets.QPushButton(Email)
        self.openFile.setGeometry(QtCore.QRect(300, 60, 93, 28))
        self.openFile.setObjectName("openFile")
        self.sendFile = QtWidgets.QPushButton(Email)
        self.sendFile.setGeometry(QtCore.QRect(300, 210, 93, 28))
        self.sendFile.setObjectName("sendFile")
        self.label_2 = QtWidgets.QLabel(Email)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pic1 = QtWidgets.QLabel(Email)
        self.pic1.setGeometry(QtCore.QRect(110, 160, 41, 41))
        self.pic1.setText("")
        self.pic1.setObjectName("pic1")
        self.textEdit = QtWidgets.QTextEdit(Email)
        self.textEdit.setGeometry(QtCore.QRect(100, 60, 191, 91))
        self.textEdit.setText("")
        self.textEdit.setObjectName("textEdit")
        self.text_pic = QtWidgets.QLabel(Email)
        self.text_pic.setGeometry(QtCore.QRect(110, 210, 81, 21))
        self.text_pic.setText("")
        self.text_pic.setObjectName("text_pic")
        self.global_path = QtWidgets.QLabel(Email)
        self.global_path.setText("") #self create a global path to take email from
        self.global_path.setObjectName("global_path")

        self.retranslateUi(Email)
        QtCore.QMetaObject.connectSlotsByName(Email)

    def retranslateUi(self, Email):
        _translate = QtCore.QCoreApplication.translate
        Email.setWindowTitle(_translate("Email", "EmailWindow"))
        self.label.setText(_translate("Email", "Send:"))
        self.openFile.setText(_translate("Email", "Open File "))
        self.sendFile.setText(_translate("Email", "Send Email"))
        self.label_2.setText(_translate("Email", "Message:"))
        self.openFile.clicked.connect(self.openfile_handler)
        self.sendFile.clicked.connect(self.sending_Email)
    def openfile_handler(self):
        #print("click")
        self.open_filedialog()

    def open_filedialog(self):# get the open dialog box
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        globalpath=path
        total=""
        typeFile=""
        if path != "":
            for x in reversed(path):#loop to get the e.g. (/xxxxxxxxx.csv) last pathname

                if x == "/":
                    break
                total+=str(x)
            for i in reversed(path): #loop to get the e.g.(.csv) last file type
                if i == ".":
                    break
                typeFile += str(i)
            total=reverse_slicing(total)
            typeFile = reverse_slicing(typeFile)
            if typeFile == "csv": # find the right file to get the right image
                pixmap = QtGui.QPixmap("img\\csvimg1.png")
                self.pic1.setPixmap(pixmap)
                self.text_pic.setText(total)
                self.global_path.setText(globalpath)
                self.pic1.show()
            elif typeFile == "txt":
                pixmap = QtGui.QPixmap("img\\txtimg1.png")
                self.pic1.setPixmap(pixmap)
                self.text_pic.setText(total)
                self.global_path.setText(globalpath)
                self.pic1.show()
            elif typeFile == "png":
                pixmap = QtGui.QPixmap("img\\imagepng.png")
                self.pic1.setPixmap(pixmap)
                self.text_pic.setText(total)
                self.global_path.setText(globalpath)
                self.pic1.show()
            elif typeFile == "pdf":
                pixmap = QtGui.QPixmap("img\\pdf1.png")
                self.pic1.setPixmap(pixmap)
                self.text_pic.setText(total)
                self.global_path.setText(globalpath)
                self.pic1.show()
            #print typeFile
            #print globalpath


    def sending_Email(self): # send email
        wrongEmail = check(self.sendAddr.text())
        if wrongEmail == False:
            apps = QtWidgets.QApplication([])

            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid Email')

            apps.exec_()
        emailfrom = "datasearchme@gmail.com"
        emailto = self.sendAddr.text()
        fileToSend = self.global_path.text()
        username = "datasearchme@gmail.com"
        password = "data@123"

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "This is the updated data set file"
        text=self.textEdit.toPlainText()
        body=MIMEText(text, "plain")
        msg.preamble = "Error sending an attachment file"
        msg.attach(body)
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            if fileToSend != "":

                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
        if fileToSend != "":
            attachment.add_header("Content-Disposition", "attachment", filename=self.text_pic.text())
            msg.attach(attachment)


        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        #print self.sendAddr.text()
        #print self.global_path.text()
        #print self.textEdit.toPlainText()
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Email = QtWidgets.QWidget()
    ui = Ui_Email()
    ui.setupUi(Email)
    Email.show()
    sys.exit(app.exec_())

