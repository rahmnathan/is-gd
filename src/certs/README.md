# Certs
Any pem-encoded certificates in this directory with a `.pem` extension will be added to the trust store of the url shortener Docker image.

Useful in certain network environments.

`empty.pem` exists to satisfy Docker build steps when no other pems are present and can be ignored.