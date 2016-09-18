"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import scrapy


def is_excluded(url, excluded):
    """Determine whether an url has been excluded. Exclude rules can be
    a string or a regex pattern.

    Parameters
    ----------
    url: string
        url to be determined
    excluded: list of string or re.compile(r'??')
        excluded patterns, can be a string or a regex pattern.

    Returns
    -------
    True is this url is excluded, False if it is not excluded

    Examples
    --------
    >>> excluded = [
        re.compile('^.*/tobeskipped/.*$'),
        'https://www.google.com/js/'
    ]
    This exclude patterns will skip urls which contains 'tobeskipped' path and
    urls who starts with https://www.google.com/js/.
    """

    for pattern in excluded:
        if isinstance(pattern, str):
            if url.startswith(pattern):
                return True
        else:
            if pattern.match(url):
                return True
    return False
