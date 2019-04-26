FROM yekingyan/python:3.6.5-mysql
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/

#FROM python:3.6-alpine
#WORKDIR /app
#COPY --from=0 /app /app
#CMD python3 manage.py runserver 0.0.0.0:8000

#EXPOSE 8000
