#!/usr/bin/python3.4

import requests


try:
    print(requests.get("http://localhost:8000/create_matches").status_code)
except:
    print("Não criei match nenhum, mals")