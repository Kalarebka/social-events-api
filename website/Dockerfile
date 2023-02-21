FROM python:3.10
 
ENV APP_HOME=/website
ENV APP_USER=django
 
RUN groupadd -g 1001 -r $APP_USER && \
    useradd -r -g $APP_USER -u 1001 $APP_USER
 
WORKDIR $APP_HOME
 
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
COPY requirements.txt .
RUN pip install -r requirements.txt
 
COPY website .
 
RUN chown -R $APP_USER:$APP_USER $APP_HOME
USER $APP_USER
