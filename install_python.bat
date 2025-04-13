@echo off
echo 正在下载Python安装程序...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'"

echo.
echo 请运行下载的python-installer.exe文件
echo 安装时请确保勾选"Add Python to PATH"选项
echo.
echo 安装完成后，请按任意键继续...
pause

echo 正在安装Python依赖...
pip install requests==2.31.0

echo.
echo 安装完成！
echo 现在可以运行 upload_historical_data.py 来上传数据
pause 