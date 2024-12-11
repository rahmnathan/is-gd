<h1>URL Shortener</h1>

[![Build Status](http://jenkins.nathanrahm.com/buildStatus/icon?job=url-shortener)](https://jenkins.nathanrahm.com/job/url-shortener/)

This project parses a file or directory of files containing urls and shortens them via the https://is.gd api.

# Requirements
Docker is required to build/run this project.

# Build
You can build a fresh Docker image by executing the following command in the project's root directory:
`docker build -t rahmnathan/url-shortener src/`

### Certificate management
If you need to provide additional ca-certificates, you can put the pem-encoded files into the `src/certs/` directory and they
will be added to the trust store during the Docker build process.

# Usage

### Shell Script
`./shorten-urls.sh <path-to-url-file-or-directory>`

#### Example
`./shorten-urls.sh ./url-files/urls1.txt`

# URL Files
See the `./url-files` directory for example url files.
