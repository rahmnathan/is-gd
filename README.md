<h1>URL Shortener</h1>

[![Build Status](http://jenkins.nathanrahm.com/buildStatus/icon?job=is-gd)](https://jenkins.nathanrahm.com/job/is-gd/)

This project parses a file or directory of files containing urls and shortens them via the https://is.gd api.

# Usage

### Shell Script
`./shorten-urls.sh <path-to-url-file-or-directory>`

#### Example
`./shorten-urls.sh ./url-files/urls1.txt`


### Docker
`docker run -it -v <path-to-url-file-or-directory>:/mnt/url-shortener/data rahmnathan/is-gd`

#### Example
`docker run -it -v ./url-files/urls1.txt:/mnt/url-shortener/data rahmnathan/is-gd`


### Python
`python3 src/shorten_urls.py <path-to-url-file-or-directory>`

#### Example
`python3 src/shorten_urls.py ./url-files/urls1.txt`


# URL Files
See the ./url-files directory for example url files.

# Development
You can build a fresh Docker image with the following command:
`docker build -t rahmnathan/is-gd src/`

### Certificate management
If you need to provide additional ca-certificates, you can put the pem-encoded files into the src/certs/ directory and they
will be added to the trust store during the Docker build process.
