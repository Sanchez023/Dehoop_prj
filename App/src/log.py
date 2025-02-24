import logging
import time
file_timestamp = str(int(time.time()))
# logging.basicConfig(level=logging.INFO,format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO,format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    ,filename=f'C:/Users/liubi/Documents/恒邦保险/代码文件/dehoop_prj/APP/Log/dehoopApi_{file_timestamp}.log',encoding="utf-8",filemode="a" )
logger = logging.getLogger(__name__)
