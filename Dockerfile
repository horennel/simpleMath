FROM python:3.10.6

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 21330

CMD ["python3", "main.py"]