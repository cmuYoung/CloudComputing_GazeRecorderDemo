kill -9 `ps -ef|grep "python3 app.py"| awk 'NR==1 {print $2}'`
nohup python3 app.py &
ps -ef |grep "python3 app.py"
