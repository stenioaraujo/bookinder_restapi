#!/usr/bin/python
#
# -*- coding: utf-8 -*-

import requests


try:
    print(requests.get("http://localhost:8844/create_matches").status_code)
except:
    print("Nao criei match nenhum, mals")
