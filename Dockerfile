FROM python:3.7.5-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 1337
ENTRYPOINT [ "python3" ]
CMD [ "api.py" ]
