import json  # For pretty-printing the response from Twitter
from requests_oauthlib import OAuth1Session  # To handle secure connection with Twitter

# Define a class for posting tweets to Twitter
class Tweet:
    _instance = None  # This is a class variable to make sure we only ever create one Tweet object (singleton pattern)

    # These are the keys provided by Twitter when you register an app on their developer platform
    CONSUMER_KEY = 'your_key'
    CONSUMER_SECRET = 'your_secret'

    # This function creates a new object if one doesn't already exist
    def __new__(cls):
        if cls._instance is None:
            print('Creating the Tweet instance...')
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.oauth = None  # This will hold our login info
            cls._instance.authenticate()  # Log in to Twitter
        return cls._instance  # Return the existing or new object

    # This method handles the login process with Twitter
    def authenticate(self):
        # This URL lets us request permission to post tweets
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(self.CONSUMER_KEY, client_secret=self.CONSUMER_SECRET)

        # Try to get temporary login tokens from Twitter
        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print("Invalid consumer key or secret.")
            return

        # Store the tokens from the response
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got request token.")

        # Build the link where the user must go to allow access
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("🔗 Please go here and authorize: ", authorization_url)

        # Ask the user to enter the code they get from Twitter
        verifier = input("Enter the PIN from Twitter: ")

        # Now that we have the PIN (verifier), we ask Twitter for the final access token
        oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )

        # Ask Twitter to give us final permission
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        # Save the tokens we'll use to tweet
        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Now we are fully authenticated and ready to tweet!
        self.oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        print("Authentication complete.")

    # This function sends a tweet
    def make_tweet(self, tweet_text):
        if not self.oauth:
            raise ValueError('Authentication failed!')  # If we aren't logged in, raise an error

        # Try to post the tweet
        response = self.oauth.post(
            "https://api.twitter.com/1.1/statuses/update.json",
            data={"status": tweet_text},  # The tweet content
        )

        # If the tweet fails, show the error
        if response.status_code != 200:
            raise Exception(
                f"Tweet failed: {response.status_code} — {response.text}"
            )

        # Tweet went through successfully
        print("Tweet posted successfully!")
        json_response = response.json()  # Get details about the tweet
        print(json.dumps(json_response, indent=4, sort_keys=True))  # Print it nicely

# This section is only used when testing directly (not when used inside a Django project)
if __name__ == "__main__":
    bot1 = Tweet()  # Create the first instance
    bot2 = Tweet()  # Try to create a second one

    # They are the same object because of the singleton pattern
    print(f"Same instance? {'Yes' if bot1 is bot2 else 'No'}")

    # Ask the user what they want to tweet
    tweet_text = input("Enter your tweet: ")
    bot1.make_tweet(tweet_text)  # Send the tweet!
