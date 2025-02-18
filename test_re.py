
import socket
def check_port(ip, port):
   # 设置超时时间为3秒钟
   socket.setdefaulttimeout(3)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
       s.connect((ip, port))
       print("端口开放")
   except socket.timeout:
       print("端口关闭")
   except ConnectionRefusedError:
       print("连接被拒绝")
   except Exception as e:
       print("发生异常：", e)
   finally:
       s.close()
 
if __name__ == '__main__':
  check_port("10.1.8.17", 30104)