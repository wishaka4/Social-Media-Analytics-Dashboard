from django.shortcuts import redirect, render
from django.http import HttpResponse
import matplotlib
import praw
from django.http import JsonResponse
from .models import RedditPost
import pandas as pd
from django.db.models import Avg, Count  # Import Avg and Count
import io
import base64
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')

# Reddit app credentials
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    user_agent="MyDjangoApp/1.0"
)

def reddit_auth(request):
    # Redirect users to Reddit authorization URL
    auth_url = reddit.auth.url(["identity"], state="random_state", duration="permanent")
    return redirect(auth_url)

def reddit_callback(request):
    # Exchange authorization code for access token
    code = request.GET.get("code")
    token = reddit.auth.authorize(code)
    
    # Use access token to fetch user profile data
    user = reddit.user.me()
    return HttpResponse(f"Logged in as: {user.name}, Link karma: {user.link_karma}, Comment karma: {user.comment_karma}")



def fetch_latest_posts(request):
    # Authenticate with Reddit API
    reddit = praw.Reddit(
        client_id="client_id",
        client_secret="client_secret",
        user_agent="MyDjangoApp/1.0"
    )

    try:
        # Fetch the latest posts from the "python" subreddit
        subreddit = reddit.subreddit("python")
        posts = subreddit.new(limit=10)

        # Extract post data
        latest_posts = []
        for post in posts:
            post_data = {
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'num_comments': post.num_comments,
                'upvote_ratio': post.upvote_ratio,
                'selftext': post.selftext,
                'link_flair_text': post.link_flair_text,
                 # Add more attributes as needed
            }
             # Create and save RedditPost instance
            reddit_post = RedditPost(
                title=post_data['title'],
                author=post_data['author'],
                score=post_data['score'],
                num_comments=post_data['num_comments'],
                upvote_ratio=post_data['upvote_ratio'],
                selftext="test",
                link_flair_text=post_data['link_flair_text']
            )
            reddit_post.save()
            latest_posts.append(post_data)

        return render(request, 'latest_posts.html', {'posts': latest_posts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def fetch_posts_by_author(request, author_name):
    # Authenticate with Reddit API
    reddit = praw.Reddit(
        client_id="client_id",
        client_secret="client_secret",
        user_agent="MyDjangoApp/1.0"
    )

    try:
        # Fetch posts authored by the specified author
        posts = reddit.redditor(author_name).submissions.new()
        latest_posts = []
        # Insert fetched post data into the database
        for post in posts:
            post_data = {
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'num_comments': post.num_comments,
                'upvote_ratio': post.upvote_ratio,
                'selftext': post.selftext,
                'link_flair_text': post.link_flair_text,
                # Add more attributes as needed
            }

            # Create and save RedditPost instance
            reddit_post = RedditPost.objects.create(
                title=post_data['title'],
                author=post_data['author'],
                score=post_data['score'],
                num_comments=post_data['num_comments'],
                upvote_ratio=post_data['upvote_ratio'],
                selftext=post_data['selftext'],
                link_flair_text=post_data['link_flair_text']
            )
            reddit_post.save()
            latest_posts.append(post_data)

        return render(request, 'author_posts.html', {'posts': latest_posts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def display_posts(request):
    # Fetch all RedditPost objects
    reddit_posts = RedditPost.objects.all()
    # Pass the fetched data to the template
    return render(request, 'posts_table.html', {'reddit_posts': reddit_posts})

def display_data_with_pandas(request):
    # Fetch data from your Django model
    reddit_posts = RedditPost.objects.all()

    # Convert the fetched data into a Pandas DataFrame
    data = {
        'title': [post.title for post in reddit_posts],
        'author': [post.author for post in reddit_posts],
        'score': [post.score for post in reddit_posts],
        'num_comments': [post.num_comments for post in reddit_posts],
        'upvote_ratio': [post.upvote_ratio for post in reddit_posts],
        'selftext': [post.selftext for post in reddit_posts],
        'link_flair_text': [post.link_flair_text for post in reddit_posts]
    }
    df = pd.DataFrame(data)

    # Display the DataFrame
    return render(request, 'display_data.html', {'df': df})

def display_data_with_demographics(request):
    # Fetch data from your Django model
    reddit_posts = RedditPost.objects.all()

    # Calculate user demographics
    unique_authors_count = reddit_posts.values('author').distinct().count()
    author_stats = reddit_posts.values('author').annotate(
        average_score=Avg('score'),
        average_num_comments=Avg('num_comments'),
        total_posts=Count('id')
    )

    context = {
        'unique_authors_count': unique_authors_count,
        'author_stats': author_stats,
    }

    return render(request, 'display_data_with_demographics.html', context)

def demographics(request):
    # Fetch data from your Django model
    reddit_posts = RedditPost.objects.all()

    # Calculate user demographics
    unique_authors_count = reddit_posts.values('author').distinct().count()
    author_stats = reddit_posts.values('author').annotate(
        average_score=Avg('score'),
        average_num_comments=Avg('num_comments'),
        total_posts=Count('id')
    )

    # Extract data for visualization
    authors = [stat['author'] for stat in author_stats]
    avg_scores = [stat['average_score'] for stat in author_stats]
    avg_num_comments = [stat['average_num_comments'] for stat in author_stats]
    total_posts = [stat['total_posts'] for stat in author_stats]

    # Plotting
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    axes[0].bar(authors, avg_scores, color='skyblue')
    axes[0].set_ylabel('Average Score')
    axes[0].set_title('Average Score by Author')

    axes[1].bar(authors, avg_num_comments, color='lightgreen')
    axes[1].set_ylabel('Average Number of Comments')
    axes[1].set_title('Average Number of Comments by Author')

    axes[2].bar(authors, total_posts, color='lightcoral')
    axes[2].set_ylabel('Total Posts')
    axes[2].set_title('Total Posts by Author')

    plt.tight_layout()

    # Convert plot to image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Embed the image in the HTML response
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    graphic_html = f'<img src="data:image/png;base64,{graphic}">'

    context = {
        'unique_authors_count': unique_authors_count,
        'author_stats': author_stats,
        'graphic': graphic_html,
    }

    return render(request, 'demographics.html', context)


def demographics1(request):
    # Fetch data from your Django model
    reddit_posts = RedditPost.objects.all()

    # Calculate user demographics
    unique_authors_count = reddit_posts.values('author').distinct().count()
    author_stats = reddit_posts.values('author').annotate(
        total_posts=Count('id')
    )

    # Extract data for visualization
    authors = [stat['author'] for stat in author_stats]
    total_posts = [stat['total_posts'] for stat in author_stats]

    # Calculate percentage of each demographic category
    percentages = [(posts / sum(total_posts)) * 100 for posts in total_posts]

    # Plotting pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(percentages, labels=authors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    ax.set_title('User Demographics')

    # Convert plot to image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Embed the image in the HTML response
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    graphic_html = f'<img src="data:image/png;base64,{graphic}">'

    context = {
        'unique_authors_count': unique_authors_count,
        'author_stats': author_stats,
        'graphic': graphic_html,
    }


    return render(request, 'demographics1.html', context)