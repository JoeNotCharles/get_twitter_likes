# Copyright 2022 Joe Mason
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import creds
import pprint
import tweepy

EXPANSIONS = [
    'author_id',
    'referenced_tweets.id',
    'in_reply_to_user_id',
    'attachments.media_keys',
]

MEDIA_FIELDS = [
    'media_key',
    'type',
    'url',
    'duration_ms',
    'height',
    'width',
    'preview_image_url',
    'alt_text',
    'variants',
]

TWEET_FIELDS = [
    'id',
    'text',
    'attachments',
    'author_id',
    'created_at',
    'lang',
    'referenced_tweets',
]

client = tweepy.Client(bearer_token=creds.bearer_token,
                       consumer_key=creds.consumer_key,
                       consumer_secret=creds.consumer_secret,
                       access_token=creds.access_token,
                       access_token_secret=creds.access_token_secret,
                       return_type=dict)


def _get_member(d, key, default):
    return key in d and d[key] or default


def get_likes():
    liked_tweets = {}
    users = {}
    media = {}
    next_token = None
    while True:
        response = client.get_liked_tweets(creds.user_id,
                                           pagination_token=next_token,
                                           expansions=EXPANSIONS,
                                           media_fields=MEDIA_FIELDS,
                                           tweet_fields=TWEET_FIELDS)
        pprint.pp(response)
        for tweet in _get_member(response, 'data', []):
            liked_tweets[tweet['id']] = tweet
        includes = _get_member(response, 'includes', {})
        for m in _get_member(includes, 'media', []):
            media[m['media_key']] = m
        for u in _get_member(includes, 'users', []):
            users[u['id']] = u
        # TODO: go through response.includes, get media info, etc.
        # tweet.data includes attachments/media_keys which should map the media info to tweets. (Same for author_id)
        # Also handle response.errors
        try:
            next_token = _get_member(response, 'meta', {})['next_token']
        except KeyError:
            break

    # Attach users and media to tweets
    for tweet in liked_tweets.values():
        if 'author_id' in tweet:
            tweet['author'] = _get_member(users, tweet['author_id'], None)
        attachments = _get_member(tweet, 'attachments', {})
        tweet['media'] = []
        for media_key in _get_member(attachments, 'media_keys', []):
            tweet['media'].append(_get_member(media, media_key, None))

    return liked_tweets
