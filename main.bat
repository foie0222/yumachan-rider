chcp 65001

set dt=%DATE:/=%
set tm=%TIME: =0%
set tm=%tm::=%
set tm=%tm:~0,6%
set TIMESTAMP=%dt%%tm%

C:\Users\foie\AppData\Local\Programs\Python\Python38-32\python.exe C:\develop\git\yumachan-rider\main.py %TIMESTAMP%
