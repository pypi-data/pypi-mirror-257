# PyClotho

A python implementation using [mitmproxy](https://mitmproxy.org/) of [Clotho](https://github.com/ClothoProxy/Clotho)

The proxy will only accept requests to amazonaws.com with a valid Authorization header.
It will filter AWS accounts, regions, and services based on the [configuration](./config.yaml.example)


## How to run

On the server
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

```


```

or using Docker 

```sh
docker run --rm -v $(pwd):/home/mitmproxy/.mitmproxy \
-p 8080:8080 mitmproxy/mitmproxy:10.2.2 mitmproxy \
-s /home/mitmproxy/.mitmproxy/clotho.py
```

On the client

```sh
export http_proxy=http//serverip:8080
export https_proxy=http://serverip:8080
aws s3 ls --no-verify-ssl
```


## Development

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

```


