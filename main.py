import praw
import openai
import random
import time
import argparse
import streamlit as st

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--client_id", required=True, help="Reddit client ID")
parser.add_argument("--client_secret", required=True, help="Reddit client secret")
parser.add_argument("--username", required=True, help="Reddit username")
parser.add_argument("--password", required=True, help="Reddit password")
parser.add_argument("--user_agent", required=True, help="Reddit user agent")
parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")
args = parser.parse_args()

# Reddit API client setup
reddit = praw.Reddit(client_id=args.client_id,
                     client_secret=args.client_secret,
                     username=args.username,
                     password=args.password,
                     user_agent=args.user_agent)

# OpenAI API client setup
openai.api_key = args.openai_api_key

# Keep track of the posts that have already been responded to
responded_posts = set()

def run_app():
    while True:
        # Get rising ELI5 posts from Reddit
        subreddit = reddit.subreddit("explainlikeimfive")
        posts = subreddit.rising(limit=5)

        # Process each rising post
        for post in posts:
            # Skip the post if it has already been responded to
            if post.id in responded_posts:
                continue

            # Generate an explanation for the post
            prompt = f"Explain the following like I'm 5: {post.title}"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text

            # Submit the explanation as a comment to the post
            post.reply(response)

            # Print the post and its explanation
            st.write("Post Title:", post.title)
            st.write("Post Explanation:", response)

            # Add the post to the list of responded posts
            responded_posts.add(post.id)

        # Sleep for a random interval between 12 minutes and 6 hours
        sleep_time = random.uniform(12 * 60, 6 * 60 * 60)
        st.write(f"Sleeping for {sleep_time / 60} minutes")
        time.sleep(sleep_time)

# Run the Streamlit app
st.set_page_config(page_title="Reddit ELI5 Responder", page_icon=":robot:", layout="wide")
st.title("Reddit ELI5 Responder")
run_app()


""""import praw
import openai
import random
import time

user_agent = "praw_scraper_1.0"
# Reddit API client setup
reddit = praw.Reddit(client_id'...'
                     client_secret='6x',
                     username='x',
                     password='x',
                     user_agent=user_agent)

# OpenAI API client setup
openai.api_key = "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"

# Keep track of the posts that have already been responded to
responded_posts = set()

while True:
    # Get rising ELI5 posts from Reddit
    subreddit = reddit.subreddit("explainlikeimfive")
    posts = subreddit.rising(limit=5)

    # Process each rising post
    for post in posts:
        # Skip the post if it has already been responded to
        if post.id in responded_posts:
            continue

        # Generate an explanation for the post
        prompt = f"Explain the following like I'm 5: {post.title}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        # Submit the explanation as a comment to the post
        post.reply(response)

        # Print the post and its explanation
        print("Post Title:", post.title)
        print("Post Explanation:", response)

        # Add the post to the list of responded posts
        responded_posts.add(post.id)

    # Sleep for a random interval between 12 minutes and 6 hours
    sleep_time = random.uniform(12 * 60, 6 * 60 * 60)
    print(f"Sleeping for {sleep_time / 60} minutes")
    time.sleep(sleep_time)"""""


