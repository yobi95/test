FROM python:3.7-alpine


WORKDIR /home/ITP4121-EA-assignment-2

ENV DATABASE_HOST=mysql

#COPY requirements.txt requirements.txt
COPY requirements.txt requirements.txt
RUN apk update && apk add --no-cache --update gcc musl-dev libffi-dev openssl-dev gfortran build-base wget libpng-dev openblas-dev libjpeg-turbo-dev && apk add mysql-client && apk add py3-scipy
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add --no-cache mariadb-dev

RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install wheel
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install configparser

RUN cp venv/bin/pip3/configparser.py venv/bin/pip3/ConfigParser.py
RUN venv/bin/pip3 install mysql-python
#RUN venv/bin/pip3 install mysql-connector

RUN venv/bin/pip3 install gunicorn

RUN venv/bin/pip3 install mysqlclient  

RUN apk del build-deps

#RUN venv/bin/pip3 install mysqlclient


COPY data data
COPY static static 
COPY templates templates
COPY main.py api_children.py api_files.py api_loginout.py api_selector.py api_status.py api_user.py funcs.py global_var.py pg_child.py pg_index.py pg_loginout.py pg_status.py pg_user.py preenv.py boot.sh config.conf db_params.py deployment2022.sh setup.sh get_preview_link.sh ttmssd.sql ./

#RUN chmod 755 setup.shd
#RUN chmod 755 get_preview_link.sh

#COPY main.py boot.sh ./

#RUN chmod +x boot.sh

ENV FLASK_APP main.py

CMD ["python3", "main.py"]

#RUN chown -R itp4121ea:itp4121ea ./

EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]
#ENTRYPOINT ["./setup.sh"]
#ENTRYPOINT ["./get_preview_link.sh"]
#ENTRYPOINT ["./deployment2022.sh"]

