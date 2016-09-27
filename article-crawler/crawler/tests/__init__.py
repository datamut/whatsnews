"""
Author: Wenhua Yang
Date: 9/24/16
"""

import os
from scrapy.http import TextResponse, Request


def fake_response(file_name, url):
    # TODO: Try to reuse this fake_response
    request = Request(url=url)
    responses_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(responses_dir, file_name)
    file_content = open(file_path, 'r').read()
    response = TextResponse(url=url, request=request, body=file_content,
                            encoding='utf-8')
    return response
