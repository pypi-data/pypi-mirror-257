#!/usr/bin/env python3

"""
This module provides simple to use access for recurring
requests to receive content either from files or URLs.

Copyright by SuperUdo3000, March 2023
Version = 0.1   (harmonized-type-1)
"""

from harmonized import chrome


def download_file(url='https://www.python.org/static/img/python-logo.png', local_filename="demo_inoutcache.png"):
    import shutil
    response = chrome.get(url, stream=True)
    with open(local_filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_contents(whatever: str, fallback_value='', http_post=False, timeout=2, auto_buffer_seconds=0, print_errors=False):
    """
    Get content of a file or url.

    :param whatever:        a <str> either 'http://....' or 'demo.txt' or '/filename.txt'
    :param fallback_value:  specify what to return in case of any error or exception, default is None

    :return:                the content of the url / file or the fallback_value
    :raises:                multiple
    """

    if isinstance(whatever, str):
        whatever = str(whatever)
        print(f'get_contents prefers whatever as type <str>. Auto casted to {whatever}')

    if whatever.lower().startswith('http'):

        # I guees it is an URL
        try:
            import os
            import time
            if auto_buffer_seconds > 0:
                # user wants to limit requests to server, very good!
                if not os.path.exists('_inoutcache'):
                    os.mkdir('_inoutcache')

                whatever_save = whatever.replace('/', '_')
                whatever_save = whatever_save.replace(':', '_')

                temp_file_path = '_inoutcache/' + whatever_save + '.txt'
                if os.path.exists(temp_file_path):

                    with open(temp_file_path, 'r') as tf:
                        lines = tf.readlines()

                        time_line = float(lines[0])
                        body = ''.join(lines[1:])

                        delta_time = time.time() - time_line
                        if delta_time < auto_buffer_seconds:
                            print(f'FROM CACHE DT={delta_time:8.1f} for {whatever[:48]}...')
                            return body

            if http_post:
                res = chrome.post(whatever, timeout=timeout)
                print('NOPE')
                # quit()
            else:
                # res = requests.get(whatever, timeout=timeout)
                res = chrome.get(whatever, timeout=timeout)
            if res.status_code != 200:
                # print(f'get_contents assumed url {whatever} return status_code {res.status_code}')
                return fallback_value

            if auto_buffer_seconds > 0:
                import time
                time_line = str(time.time()) + '\n'
                write(temp_file_path, time_line + res.text)

            return res.text
        except Exception as e:
            if print_errors:
                print(f'get_contents assumed url {whatever} failes with {e}')
            return fallback_value

    else:  # '/' in whatever:
        # I guess it is a file or path to a file
        import os
        if not os.path.exists(whatever):
            print(f'get_contents assumed file {whatever} not found')
            return fallback_value

        with open(whatever, 'r', encoding="latin-1") as filet:
            return filet.read()

        print(f'get_contents error for whatever {whatever}')
        return fallback_value


def get_data_from_json(whatever: str, fallback_value='', auto_buffer_seconds=0):
    """
    :return:    Data Object
    """
    import json
    content = get_contents(whatever=whatever, fallback_value=None, auto_buffer_seconds=auto_buffer_seconds)
    if content is not None:
        return json.loads(content)
    else:
        return fallback_value


def write(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        return True


def append(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')
        return True


if __name__ == '__main__':
    t1 = get_contents('http://python.org/', auto_buffer_seconds=10)
