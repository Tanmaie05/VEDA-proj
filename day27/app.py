
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://dummyjson.com/posts/{}"


def fetch_post(post_id):
    try:
        response = requests.get(
            API_URL.format(post_id),
            timeout=10
        )

        if response.status_code == 404:
            return None, "Post not found. Enter a valid post ID."

        response.raise_for_status()
        data = response.json()

        post = {
            "id": data.get("id"),
            "title": data.get("title", "No title available"),
            "body": data.get("body", "No content available"),
            "userId": data.get("userId", "Unknown"),
            "tags": data.get("tags", []),
            "views": data.get("views", "N/A")
        }

        return post, None

    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return None, "Connection failed. Check your internet."

    except requests.exceptions.HTTPError:
        return None, "The API returned an error."

    except (requests.exceptions.RequestException, ValueError):
        return None, "Unable to read the API response."


@app.route("/", methods=["GET", "POST"])
def index():
    post = None
    error = None
    post_id_value = ""

    if request.method == "POST":
        post_id_value = request.form.get("post_id", "").strip()

        try:
            post_id = int(post_id_value)

            if post_id < 1:
                error = "Enter a post ID greater than zero."
            else:
                post, error = fetch_post(post_id)

        except ValueError:
            error = "Please enter a valid whole-number ID."

    return render_template(
        "index.html",
        post=post,
        error=error,
        post_id_value=post_id_value
    )


if __name__ == "__main__":
    app.run(debug=True)
