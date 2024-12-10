FROM python:3

WORKDIR /usr/src/is-gd

# Point Python requests to default ca bundle
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Load additional certificates
COPY certs/*.pem ./
RUN cat *.pem >> $REQUESTS_CA_BUNDLE

# Install app requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY shorten_urls.py ./

CMD ["python3", "shorten_urls.py", "/mnt/url-shortener/data"]
