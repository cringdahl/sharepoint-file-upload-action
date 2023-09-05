FROM python:3.11-alpine
HEALTHCHECK NONE
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
USER 1000

COPY src/send_to_sharepoint.py /usr/src/app/
# full path is necessary or it defaults to main branch copy
ENTRYPOINT [ "python", "/usr/src/app/send_to_sharepoint.py" ]