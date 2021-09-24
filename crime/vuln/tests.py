import hashlib

from django.test import TestCase
from django.test import TestCase
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from screecher.utils import error_status

import requests
import string
import time

# Create your tests here.

charset = "abcdef0123456789"

s = requests.Session()
s.get('https://crime.jeopardy.websec.saarland/')
for i in charset:

    data = "SWAG{dbb747243e5e}" + i
    res = s.post("https://crime.jeopardy.websec.saarland/",
                 data=dict(message=data))
    tmp = res.text.index("Your message was")
    leak = res.text[tmp:tmp + 40]
    for j in leak.split():
        if j.isdigit():
            flag = int(j)
            print(flag, i)

sd = "SWAG{%s}" % hashlib.sha3_256(b"SWAG{dbb747243e5e}").hexdigest()
print(sd)