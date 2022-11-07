# Copyright 2022 Joe Mason
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import collections
import creds
import json
import sys
import tweepy
import util

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


def get_next_page(next_token, page, all_liked_tweets, all_included_tweets, all_users, all_media):
    liked_tweets = {}
    included_tweets = {}
    users = {}
    media = {}
    try:
        response = client.get_liked_tweets(creds.user_id,
                                           pagination_token=next_token,
                                           expansions=EXPANSIONS,
                                           media_fields=MEDIA_FIELDS,
                                           tweet_fields=TWEET_FIELDS)
        for tweet in util.get_dict_member(response, 'data', []):
            liked_tweets[tweet['id']] = tweet
        includes = util.get_dict_member(response, 'includes', {})
        for m in util.get_dict_member(includes, 'media', []):
            media[m['media_key']] = m
        for u in util.get_dict_member(includes, 'users', []):
            users[u['id']] = u
        for t in util.get_dict_member(includes, 'tweets', []):
            included_tweets[t['id']] = t
    except:
        print("Error on page {}, last pagination token {}".format(
              page, next_token))
        return None
    all_liked_tweets.update(liked_tweets)
    all_included_tweets.update(included_tweets)
    all_users.update(users)
    all_media.update(media)
    return util.get_dict_member(
        response, 'meta', {}).get('next_token', None)


def get_likes():
    liked_tweets = {}
    included_tweets = {}
    users = {}
    media = {}

    page = 1
    next_token = get_next_page(
        None, page, liked_tweets, included_tweets, users, media)
    while next_token:
        page += 1
        next_token = get_next_page(
            next_token, page, liked_tweets, included_tweets, users, media)

    # Embed attachment data in tweets
    for tweet in liked_tweets.values():
        if 'author_id' in tweet:
            tweet['author'] = util.get_dict_member(
                users, tweet['author_id'], None)
        attachments = util.get_dict_member(tweet, 'attachments', {})
        tweet['media'] = []
        for media_key in util.get_dict_member(attachments, 'media_keys', []):
            tweet['media'].append(util.get_dict_member(media, media_key, None))
        references = collections.defaultdict(list)
        referenced_tweets = util.get_dict_member(
            tweet, 'referenced_tweets', [])
        for reference in referenced_tweets:
            ref_type = reference['type']
            ref_id = reference['id']
            references[ref_type].append(
                util.get_dict_member(included_tweets, ref_id, None))
        tweet['references'] = dict(references)

    return liked_tweets


if __name__ == '__main__':
    tweets = get_likes()
    with open(sys.argv[1], 'w') as f:
        json.dump(tweets, f, indent=2, sort_keys=True)
