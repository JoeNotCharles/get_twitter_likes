# Copyright 2022 Joe Mason
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import json
import os.path
import shutil
import sys
import urllib.parse
import urllib.request
import util


def download_media(media_dict, key, path):
    if not key in media_dict:
        return
    url = media_dict[key]
    try:
        filename = os.path.basename(urllib.parse.urlparse(url).path)
        os.makedirs(path, exist_ok=True)
        with urllib.request.urlopen(url) as response:
            with open(os.path.join(path, filename), 'wb') as f:
                shutil.copyfileobj(response, f)
    except:
        print("Failed to download {} to path {}".format(url, path))

def get_media(tweets):
    for tweet_id in tweets:
        tweet = tweets[tweet_id]
        for m in util.get_dict_member(tweet, 'media', []):
            media_type = m['type']
            path = os.path.join('resources', tweet_id,
                                media_type, m['media_key'])
            if media_type == 'video':
                download_media(m, 'preview_image_url', path)
                for variant in util.get_dict_member(m, 'variants', []):
                    download_media(variant, 'url', path)
            elif media_type == 'photo':
                download_media(m, 'url', path)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        tweets = json.load(f)
        get_media(tweets)
