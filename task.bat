chcp 65001

C:\Users\foie\AppData\Local\Programs\Python\Python38-32\python.exe C:\develop\git\yumachan-rider\task.py
SCHTASKS /Create /tn 中央競馬投票 /RU %1 /RP %2 /XML C:\develop\git\yumachan-rider\xml\中央競馬投票.xml /F