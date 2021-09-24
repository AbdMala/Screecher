from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import zlib

HTTP_POST_BODY = """
POST /some_url HTTP/1.1
Host: test.com
Secret: %s 

%s
"""

FLAG = "SWAG{it_would_be_a_crime_if_you_can_not_steal_me}"


@csrf_exempt
def compress(request):
    post_body = ''
    post_message = ''
    if request.method == 'POST':
        post_message = request.POST.get("message", None)
        post_body = HTTP_POST_BODY % (FLAG, post_message)
        post_body = zlib.compress(bytes(post_body, 'ascii'), 1)
    return render(request, 'compress.html', context={'message_length': len(post_body), 'message': post_message})
