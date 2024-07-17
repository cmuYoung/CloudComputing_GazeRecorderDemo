kill -9 `ps -ef|grep "python3 /home/ec2-user/git/CloudComputing_GazeRecorderDemo/app.py"| awk 'NR==1 {print $2}'`
kill -9 `ps -ef|grep "python3 app.py"| awk 'NR==1 {print $2}'`
kill -9 `ps -ef|grep "streamlit run streamlit_chart.py"| awk 'NR==1 {print $2}'`
nohup python3 app.py &
nohup streamlit run streamlit_chart.py &
ps -ef |grep "python3 app.py"
ps -ef |grep "streamlit run streamlit_chart.py"
