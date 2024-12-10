FROM python:3

WORKDIR /usr/src/is-gd

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY shorten_urls.py ./

CMD ["python3", "shorten_urls.py", "/mnt/url-shortener/data"]
