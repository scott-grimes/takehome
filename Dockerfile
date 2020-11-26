FROM python:3.7-stretch

# Requirements Layer
COPY requirements.txt /srv/
WORKDIR /srv
RUN pip install -r requirements.txt

# Production would not copy everything blindly
COPY * /srv/

EXPOSE 5000
ENTRYPOINT ["/srv/entrypoint.sh"]
