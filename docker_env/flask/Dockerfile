FROM python:3.8
WORKDIR /backend
COPY ./backend/ .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
CMD ["python","app.py"]
