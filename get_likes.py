# Copyright 2022 Joe Mason
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import creds
import tweepy

client = tweepy.Client(bearer_token=creds.bearer_token, consumer_key=creds.consumer_key,
                       consumer_secret=creds.consumer_secret, access_token=creds.access_token, access_token_secret=creds.access_token_secret)


def get_likes():
    expansions = [
        'author_id',
        'referenced_tweets.id',
        'in_reply_to_user_id',
        'attachments.media_keys',
        'attachments.poll_ids',
        'entities.mentions.username',
        'referenced_tweets.id.author_id',
    ]
    media_fields = [
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
    tweet_fields = [
        'id',
        'text',
        'attachments',
        'author_id',
        'conversation_id',
        'created_at',
        'entities',
        'in_reply_to_user_id',
        'lang',
        'referenced_tweets',
    ]
    liked_tweets = {}
    next_token = None
    while True:
        response = client.get_liked_tweets(
            creds.user_id, pagination_token=next_token, expansions=expansions)
        if response.data:
            for tweet in response.data:
                liked_tweets[tweet.id] = tweet
        # TODO: go through response.includes, get media info, etc.
        # tweet.data includes attachments/media_keys which should map the media info to tweets. (Same for author_id)
        # Also handle response.errors
        try:
            next_token = response.meta['next_token']
        except KeyError:
            break
    return liked_tweets
