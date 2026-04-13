import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, jsonify, session, abort, send_from_directory
from pymongo import MongoClient, ReturnDocument
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from urllib.parse import urlparse
from bson import ObjectId

load_dotenv()

app = Flask(__name__, static_folder="./Pages 2", static_url_path="")
app.secret_key = os.getenv("SESSION_SECRET", "change-me")

# MongoDB setup (add this block)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "skillhub")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

users = db["users"]
posts = db["posts"]
resources = db["resources"]
comments = db["comments"]

# Optional but recommended for category logic
HOBBY_TO_CATEGORY = {
    "football": "Football",
    "coding": "Coding",
    "cooking": "Cooking",
    "aitools": "AI Tools",
}
CATEGORY_TO_HOBBY = {v: k for k, v in HOBBY_TO_CATEGORY.items()}

# Upload config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_HOBBIES = {"football", "coding", "cooking", "aitools"}

# Helper purpose: Validate uploaded filename extension against allowed image types.
# Data handled: input filename string -> boolean result.
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper purpose: Validate external link format for resource posts.
# Data handled: input URL string -> boolean result (http/https with hostname).
def is_valid_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

# Helper purpose: Validate resource form input before MongoDB insert.
# Data handled:
# - Input: Flask form/files (title, description, hobby, link, image)
# - Output: list of validation error messages (empty list if valid)
def validate_resource_form(form, files):
    errors = []

    title = (form.get("title") or "").strip()
    description = (form.get("description") or "").strip()
    hobby = (form.get("hobby") or "").strip().lower()
    link = (form.get("link") or "").strip()
    image = files.get("image")

    # Mandatory fields
    if not title:
        errors.append("Title is required.")
    elif len(title) > 120:
        errors.append("Title must be 120 characters or fewer.")

    if not description:
        errors.append("Description is required.")
    elif len(description) > 2000:
        errors.append("Description must be 2000 characters or fewer.")

    if hobby not in ALLOWED_HOBBIES:
        errors.append("Invalid hobby/category.")

    # Optional link format
    if link and not is_valid_http_url(link):
        errors.append("Link must be a valid http/https URL.")

    # Optional image format
    if image and image.filename and not allowed_file(image.filename):
        errors.append("Invalid image type. Allowed: png, jpg, jpeg, gif, webp.")

    return errors

# Helper purpose: Enforce authenticated access for protected pages/API routes.
# Data handled:
# - Input: Flask session + request path
# - Output: allow request, API 401, or redirect to /signin
def require_auth(api=False):
    if "user_id" in session:
        return
    if api or request.path.startswith("/api/"):
        abort(401)
    return redirect("/signin")

# Route purpose: Default entry point; redirects user to sign-in page.
# Data handled: no body/query; returns redirect response.
@app.get("/")
def home():
    return redirect("/signin")


# Page routes

# Route purpose: Serve sign-in page HTML.
# Data handled: no DB read/write.
@app.get("/signin")
def signin_page():
    return send_from_directory(app.static_folder, "signIn.html")

# Route purpose: Serve sign-up page HTML.
# Data handled: no DB read/write.
@app.get("/signup")
def signup_page():
    return send_from_directory(app.static_folder, "signUp.html")

# Route purpose: Serve landing page HTML.
# Data handled: no DB read/write.
@app.get("/landing")
def landing_page():
    return send_from_directory(app.static_folder, "landingPage.html")

# Route purpose: Serve profile page HTML for authenticated users.
# Data handled: reads session auth state only.
@app.get("/profile")
def profile_page():
    require_auth()
    return send_from_directory(app.static_folder, "profilePage.html")

# Route purpose: Serve support page HTML.
# Data handled: no DB read/write.
@app.get("/support")
def support_page():
    return send_from_directory(app.static_folder, "supportPage.html")

# Route purpose: Serve Football hobby page HTML.
# Data handled: no DB read/write.
@app.get("/football")
def football_page():
    return send_from_directory(app.static_folder, "Football.html")

# Route purpose: Serve Coding hobby page HTML.
# Data handled: no DB read/write.
@app.get("/coding")
def coding_page():
    return send_from_directory(app.static_folder, "Coding.html")

# Route purpose: Serve Cooking hobby page HTML.
# Data handled: no DB read/write.
@app.get("/cooking")
def cooking_page():
    return send_from_directory(app.static_folder, "Cooking.html")

# Route purpose: Serve AI Tools hobby page HTML.
# Data handled: no DB read/write.
@app.get("/aitools")
def ai_tools_page():
    return send_from_directory(app.static_folder, "AITools.html")


# Legacy compatibility routes

# Route purpose: Redirect old signIn.html path to canonical /signin.
# Data handled: redirect only.
@app.get("/signIn.html")
def legacy_signin():
    return redirect("/signin")

# Route purpose: Redirect old signUp.html path to canonical /signup.
# Data handled: redirect only.
@app.get("/signUp.html")
def legacy_signup():
    return redirect("/signup")

# Route purpose: Redirect old landingPage.html path to canonical /landing.
# Data handled: redirect only.
@app.get("/landingPage.html")
def legacy_landing():
    return redirect("/landing")

# Route purpose: Redirect old profilePage.html path to canonical /profile.
# Data handled: redirect only.
@app.get("/profilePage.html")
def legacy_profile():
    return redirect("/profile")

# Route purpose: Redirect old supportPage.html path to canonical /support.
# Data handled: redirect only.
@app.get("/supportPage.html")
def legacy_support():
    return redirect("/support")

# Route purpose: Redirect old Football.html path to canonical /football.
# Data handled: redirect only.
@app.get("/Football.html")
def legacy_football():
    return redirect("/football")

# Route purpose: Redirect old Coding.html path to canonical /coding.
# Data handled: redirect only.
@app.get("/Coding.html")
def legacy_coding():
    return redirect("/coding")

# Route purpose: Redirect old Cooking.html path to canonical /cooking.
# Data handled: redirect only.
@app.get("/Cooking.html")
def legacy_cooking():
    return redirect("/cooking")

# Route purpose: Redirect old AITools.html path to canonical /aitools.
# Data handled: redirect only.
@app.get("/AITools.html")
def legacy_aitools():
    return redirect("/aitools")

# Route purpose: Create a new user account.
# Data handled:
# - Input: form fields (fullname, username, password, confirmPassword, email)
# - MongoDB: users collection read for duplicates + insert user document
# - Output: session set + redirect /landing, or 400 on validation errors
@app.post("/signup")
def signup():
    fullname = request.form.get("fullname", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirmPassword", "")
    email = request.form.get("email", "").strip().lower()

    if not fullname or not username or not password or not email:
        return "Missing required fields", 400
    if password != confirm:
        return "Passwords do not match", 400
    if users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return "Username or email already exists", 400

    user_id = users.insert_one({
        "fullname": fullname,
        "username": username,
        "password": generate_password_hash(password),
        "email": email,
        "createdAt": datetime.utcnow()
    }).inserted_id

    session["user_id"] = str(user_id)
    return redirect("/landing")


# Route purpose: Authenticate existing user.
# Data handled:
# - Input: form fields (username, password)
# - MongoDB: users collection read by username
# - Output: session set + redirect /landing, or 401 if invalid
@app.post("/signin")
def signin():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return "Invalid username or password", 401

    session["user_id"] = str(user["_id"])
    return redirect("/landing")


# Route purpose: Log user out by clearing session.
# Data handled: session clear only.
@app.get("/logout")
def logout():
    session.clear()
    return redirect("/signin")


# Route purpose: Create a text post in selected topic.
# Data handled:
# - Input: path topic + form (title, content)
# - MongoDB: posts collection insert
# - Output: redirect to topic feed
@app.post("/posts/<topic>/create")
def create_post(topic):
    require_auth()
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        return "Title and content required", 400

    posts.insert_one({
        "topic": topic.lower(),
        "title": title,
        "content": content,
        "authorId": ObjectId(session["user_id"]),
        "comments": [],
        "createdAt": datetime.utcnow()
    })
    return redirect(f"/{topic.lower()}")


# Route purpose: Serve uploaded media files by filename.
# Data handled: file path segment -> static file response from uploads folder.
@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Route purpose: Serve edit-profile page HTML (auth required).
# Data handled: session auth state only.
@app.get("/editprofile")
def edit_profile_page():
    require_auth()
    return send_from_directory(app.static_folder, "editProfile.html")


# Route purpose: Return current user's profile data as JSON.
# Data handled:
# - Input: session user_id
# - MongoDB: users collection find_one projection
# - Output: JSON profile fields
@app.get("/api/profile")
def get_profile():
    require_auth()
    user = users.find_one(
        {"_id": ObjectId(session["user_id"])},
        {"fullname": 1, "bio": 1, "hobbies": 1, "profileImage": 1, "education": 1, "favoriteFood": 1}
    )
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "fullname": user.get("fullname", ""),
        "bio": user.get("bio", ""),
        "hobbies": user.get("hobbies", []),
        "profileImage": user.get("profileImage", ""),
        "education": user.get("education", ""),
        "favoriteFood": user.get("favoriteFood", "")
    })

# Route purpose: Create/update current user's profile fields and image.
# Data handled:
# - Input: profile form fields + optional profileImage file
# - MongoDB: users collection update_one ($set)
# - Output: redirect /profile
@app.post("/profile")
def save_profile():
    require_auth()
    fullname = request.form.get("fullname", "").strip()
    bio = request.form.get("bio", "").strip()
    education = request.form.get("education", "").strip()
    favoriteFood = request.form.get("favoriteFood", "").strip()
    hobbies_raw = request.form.get("hobbies", "").strip()

    hobbies = [h.strip() for h in hobbies_raw.split(",") if h.strip()]

    update_doc = {
        "bio": bio,
        "education": education,
        "favoriteFood": favoriteFood,
        "hobbies": hobbies,
        "updatedAt": datetime.utcnow()
    }
    if fullname:
        update_doc["fullname"] = fullname

    file = request.files.get("profileImage")
    if file and file.filename:
        if not allowed_file(file.filename):
            return "Invalid image type", 400
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        update_doc["profileImage"] = f"/uploads/{filename}"

    users.update_one({"_id": ObjectId(session["user_id"])}, {"$set": update_doc})
    return redirect("/profile")

# Route purpose: Delete current user's account.
# Data handled:
# - Input: session user_id
# - MongoDB: users collection delete_one
# - Output: session clear + redirect /signup
@app.post("/profile/delete")
def delete_profile():
    require_auth()
    users.delete_one({"_id": ObjectId(session["user_id"])})
    session.clear()
    return redirect("/signup")


# Route purpose: Search hobbies by name and matching resource content.
# Data handled:
# - Input: query param q
# - MongoDB: resources collection find + count_documents
# - Output: JSON list [{slug, name, url, resourceCount}]
@app.get("/api/search/hobbies")
def search_hobbies():
    q = request.args.get("q", "").strip()
    regex = {"$regex": re.escape(q), "$options": "i"} if q else None

    matched = set()

    # Name/slug match
    for slug, display in HOBBY_TO_CATEGORY.items():
        if not q or q.lower() in slug.lower() or q.lower() in display.lower():
            matched.add(slug)

    # Resource title/description match -> map back to hobby/category
    if q:
        docs = resources.find(
            {"$or": [{"title": regex}, {"description": regex}]},
            {"hobby": 1, "category": 1}
        )
        for d in docs:
            hobby_slug = d.get("hobby")
            if hobby_slug in HOBBY_TO_CATEGORY:
                matched.add(hobby_slug)
                continue
            category = d.get("category")
            if category in CATEGORY_TO_HOBBY:
                matched.add(CATEGORY_TO_HOBBY[category])

    result = []
    for slug in sorted(matched):
        category_name = HOBBY_TO_CATEGORY[slug]
        count = resources.count_documents({
            "$or": [{"hobby": slug}, {"category": category_name}]
        })
        result.append({
            "slug": slug,
            "name": category_name,
            "url": f"/{slug}",
            "resourceCount": count
        })

    return jsonify(result)


# Route purpose: Return resources for one hobby, optionally filtered by search text.
# Data handled:
# - Input: path hobby, query q
# - MongoDB: resources collection find/sort
# - Output: JSON resource list with normalized IDs and currentUserVote
@app.get("/api/resources/<hobby>")
def get_resources(hobby):
    hobby_lower = hobby.strip().lower()
    category_name = HOBBY_TO_CATEGORY.get(hobby_lower)
    if not category_name:
        return jsonify([])

    q = request.args.get("q", "").strip()
    category_filter = {"$or": [{"hobby": hobby_lower}, {"category": category_name}]}

    if q:
        regex = {"$regex": re.escape(q), "$options": "i"}
        query = {"$and": [category_filter, {"$or": [{"title": regex}, {"description": regex}]}]}
    else:
        query = category_filter

    docs = list(resources.find(
        query,
        {"_id": 1, "title": 1, "description": 1, "image": 1, "link": 1, "authorId": 1, "createdAt": 1, "votes": 1, "userVotes": 1, "category": 1}
    ).sort("createdAt", -1))

    current_user_id = None
    if "user_id" in session:
        try:
            current_user_id = str(ObjectId(session["user_id"]))
        except Exception:
            current_user_id = None

    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["authorId"] = str(doc.get("authorId", ""))
        doc["votes"] = int(doc.get("votes", 0))
        doc["category"] = doc.get("category", category_name)

        user_votes = doc.get("userVotes", {})
        if isinstance(user_votes, dict) and current_user_id:
            doc["currentUserVote"] = int(user_votes.get(current_user_id, 0))
        else:
            doc["currentUserVote"] = 0

        doc.pop("userVotes", None)

    return jsonify(docs)


# Route purpose: Create a new resource (title/description/link/image) for a hobby.
# Data handled:
# - Input: multipart form (title, description, hobby, link, image?)
# - MongoDB: resources collection insert_one
# - Output: redirect to hobby page or JSON validation error
@app.post("/api/resources/create")
def create_resource():
    require_auth(api=True)

    errors = validate_resource_form(request.form, request.files)
    if errors:
        return jsonify({"error": " ".join(errors)}), 400

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    hobby = request.form.get("hobby", "").strip().lower()
    link = request.form.get("link", "").strip()
    image = request.files.get("image")

    image_path = ""
    if image and image.filename:
        filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        image_path = f"/uploads/{filename}"

    resources.insert_one({
        "title": title,
        "description": description,
        "hobby": hobby,
        "category": HOBBY_TO_CATEGORY.get(hobby, hobby.title()),
        "link": link,
        "image": image_path,
        "authorId": ObjectId(session["user_id"]),
        "votes": 0,
        "userVotes": {},
        "createdAt": datetime.utcnow()
    })

    return redirect(f"/{hobby}")


# Route purpose: Toggle upvote/downvote for authenticated user on a resource.
# Data handled:
# - Input: path resource_id, JSON {type: "up"|"down"}
# - MongoDB: resources find_one + find_one_and_update (votes/userVotes)
# - Output: JSON {votes, userVote}
@app.post("/api/resources/<resource_id>/vote")
def vote_resource(resource_id):
    require_auth(api=True)

    payload = request.get_json(silent=True) or {}
    vote_type = payload.get("type")
    if vote_type not in ("up", "down"):
        return jsonify({"error": "Invalid vote type"}), 400

    try:
        rid = ObjectId(resource_id)
        user_id_str = str(ObjectId(session["user_id"]))
    except Exception:
        return jsonify({"error": "Invalid id"}), 400

    doc = resources.find_one({"_id": rid}, {"votes": 1, "userVotes": 1})
    if not doc:
        return jsonify({"error": "Resource not found"}), 404

    user_votes = doc.get("userVotes", {})
    if not isinstance(user_votes, dict):
        user_votes = {}

    current_vote = int(user_votes.get(user_id_str, 0))

    if vote_type == "up":
        new_vote = 0 if current_vote == 1 else 1
    else:  # down
        new_vote = 0 if current_vote == -1 else -1

    vote_diff = new_vote - current_vote

    update_ops = {"$inc": {"votes": vote_diff}}
    if new_vote == 0:
        update_ops["$unset"] = {f"userVotes.{user_id_str}": ""}
    else:
        update_ops["$set"] = {f"userVotes.{user_id_str}": new_vote}

    updated = resources.find_one_and_update(
        {"_id": rid},
        update_ops,
        return_document=ReturnDocument.AFTER,
        projection={"votes": 1}
    )

    return jsonify({"votes": int(updated.get("votes", 0)), "userVote": new_vote})

@app.get("/api/resources/<resource_id>")
def get_resource(resource_id):
    try:
        rid = ObjectId(resource_id)
    except Exception:
        return jsonify({"error": "Invalid resource id"}), 400

    doc = resources.find_one({"_id": rid})
    if not doc:
        return jsonify({"error": "Resource not found"}), 404

    doc["_id"] = str(doc["_id"])
    doc["authorId"] = str(doc.get("authorId", ""))
    doc["votes"] = int(doc.get("votes", 0))
    doc["currentUserVote"] = 0

    if "user_id" in session:
        user_votes = doc.get("userVotes", {})
        if isinstance(user_votes, dict):
            doc["currentUserVote"] = int(user_votes.get(str(ObjectId(session["user_id"])), 0))

    doc.pop("userVotes", None)
    return jsonify(doc)

@app.get("/api/resources/<resource_id>/comments")
def get_resource_comments(resource_id):
    try:
        rid = ObjectId(resource_id)
    except Exception:
        return jsonify({"error": "Invalid resource id"}), 400

    docs = list(comments.find({"resourceId": rid}).sort("createdAt", 1))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["resourceId"] = str(doc["resourceId"])
        doc["authorId"] = str(doc.get("authorId", ""))
    return jsonify(docs)

@app.post("/api/resources/<resource_id>/comments")
def add_resource_comment(resource_id):
    require_auth(api=True)

    try:
        rid = ObjectId(resource_id)
    except Exception:
        return jsonify({"error": "Invalid resource id"}), 400

    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Comment cannot be empty"}), 400
    if len(text) > 1000:
        return jsonify({"error": "Comment too long"}), 400

    user = users.find_one(
        {"_id": ObjectId(session["user_id"])},
        {"username": 1}
    )

    comment_doc = {
        "resourceId": rid,
        "authorId": ObjectId(session["user_id"]),
        "authorName": user.get("username", "User") if user else "User",
        "text": text,
        "createdAt": datetime.utcnow(),
    }

    inserted = comments.insert_one(comment_doc)
    comment_doc["_id"] = str(inserted.inserted_id)
    comment_doc["resourceId"] = str(comment_doc["resourceId"])
    comment_doc["authorId"] = str(comment_doc["authorId"])

    return jsonify(comment_doc), 201

@app.errorhandler(401)
def handle_401(err):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Unauthorized"}), 401
    return redirect("/signin")

@app.errorhandler(404)
def handle_404(err):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not Found"}), 404
    return send_from_directory(app.static_folder, "404.html"), 404

@app.errorhandler(500)
def handle_500(err):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Server Error"}), 500
    return send_from_directory(app.static_folder, "500.html"), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)