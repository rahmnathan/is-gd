#!/usr/bin/env sh

path="$1"

print_usage(){
  echo "Usage: ./shorten_urls.sh /home/user/urls.txt"
}

# Validate path was provided
if [ -z "$path" ]; then
  print_usage
  exit 1
fi

# Validate path exists
if [ ! -f "$path" ] && [ ! -d "$path" ]; then
    echo "Path $path not found."
    print_usage
    exit 1
fi


docker run -it -v "$1":/mnt/url-shortener/data rahmnathan/is-gd
