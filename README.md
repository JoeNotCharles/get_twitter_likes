# get_twitter_likes

## Installation requirements:

 1. python3
 1. tweepy (easiest with `pip3 install tweepy`)

## One-time setup:

 1. Sign up for a Twitter developer account(https: // developer.twitter.com/)
 1. Create a new app.
 1. Go to "Keys and tokens" / "Access Token and Secret", and click "Generate",
    which will open a popup with all your tokens.
    * "Access Token" should be something like 1234567890-abc123XYZ. The part
      before the dash, which is all numbers, is your user ID.
 1. Copy all the values from the popup into creds.py:
   
    ```
    user_id = 'User ID (numeric part of Access Token)'
    consumer_key = 'API Key'
    consumer_secret = 'API Key Secret'
    bearer_token = 'Bearer Token'
    access_token = 'Access Token'
    access_token_secret = 'Access Token Secret'

## To use:

 * `python3 get_likes.py <filename.json>`
   * Downloads all your likes and saves them in the given JSON file. 
 
 * `python3 get_media.py <filename.json>`
   * Scans a file saved with `get_likes.py` for links to photos and videos,
     downloads them and saves them to disk in a directory named `resources`.