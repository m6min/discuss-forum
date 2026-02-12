import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, abort, session
from flask_sqlalchemy import SQLAlchemy

# load env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_key')
# Default ADMIN PASSWORD
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '1234')
# Enter your name
AUTHOR_NAME = 'Mümin'
# Database settings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Topic(db.Model):
    """Database Class for Topics"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20))
    ip_address = db.Column(db.String(50), default="Unknown")

    def __repr__(self):
        return f"<Topic {self.title}>"


class Message(db.Model):
    """Database Class for Messages"""

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20))
    ip_address = db.Column(db.String(50), default="Unknown")
    # Relationship, w cascade
    topic = db.relationship('Topic', backref=db.backref('messages',
                                                    lazy=True, cascade="all, delete"))


@app.context_processor
def inject_year():
    """Writes the dynamic Year on the footer"""
    return {"year": datetime.now().year}

# Paths

@app.route("/")
def index():
    """Main (index) page"""
    topics = Topic.query.all()
    return render_template("index.html", all_topics=topics[::-1])


@app.route("/contact")
def contact():
    """Contact Page"""
    return render_template("contact.html")

@app.route("/search_topics", methods=["GET", "POST"])
def search_topics():
    """Topic Searching Page"""
    searched_topic = request.args.get("searched_topic")
    founded_topics = []

    if searched_topic:
        # Filter
        founded_topics = Topic.query.filter(
            Topic.title.ilike(f"%{searched_topic}%")
        ).all()
        if not founded_topics:
            return render_template(
                "no_topic_founded.html", searched_topic=searched_topic
            )
    else:
        # If there is no search get all topics
        founded_topics = Topic.query.all()

    return render_template(
        "search_topics.html", results=founded_topics[::-1], query=searched_topic
    )


@app.route("/create_topic", methods=["GET", "POST"])
def create_topic():
    """Topic Creating Page"""
    if request.method == "POST":
        title = request.form.get("topic_title")
        content = request.form.get("topic_content")

        if not title or title.strip() == "":
            return "Topic name cannot be empty!", 400
        if not content or content.strip() == "":
            return "Message cannot be empty!", 400

        today = datetime.today()
        date_str = today.strftime("%d/%m/%Y")
        client_ip = request.remote_addr
        new_topic = Topic(
            title=title, content=content, date=date_str, ip_address=client_ip
        )

        try:
            db.session.add(new_topic)
            db.session.commit()
            return redirect(url_for("topic", topic_id=new_topic.id))
        except Exception as e:
            print(f"Error: {e}")
            return (
                "Oops.. There is something wrong. Please try again or check console logs.",
                500,
            )

    return render_template("create_topic.html")


@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    """Topic Detailed Page"""
    current_topic = Topic.query.get_or_404(topic_id)
    messages = current_topic.messages[::-1]
    return render_template("topic.html", topic=current_topic, msgs=messages)


@app.route("/rules")
def rules():
    """Rule Page"""
    return render_template("rules.html")


@app.route("/add_message/<int:topic_id>", methods=["GET", "POST"])
def add_message(topic_id):
    """Add Thoughts Page"""
    current_topic = Topic.query.get_or_404(topic_id)

    if request.method == "POST":
        input_content = request.form.get("message")
        if input_content and input_content.strip():
            today = datetime.today()
            date_str = today.strftime("%d/%m/%Y")
            client_ip = request.remote_addr

            new_message = Message(
                topic_id=topic_id,
                content=input_content,
                date=date_str,
                ip_address=client_ip,
            )
            db.session.add(new_message)
            db.session.commit()

            return render_template(
                "result.html", input_content=input_content, topic_id=topic_id
            )
        else:
            abort(400)

    return render_template(
        "add_message.html", title=current_topic.title, topic_id=topic_id
    )

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    """ Admin Login Page / Controls """
    if request.method == "POST":
        input_pass = request.form.get("password_input")
        if input_pass == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for("admin"))
        else:
            abort(404)
    return render_template("admin_login.html", author_name = AUTHOR_NAME)

@app.route("/admin")
def admin():
    """ Admin Panel Page """
    if not session.get('admin_logged_in'):
        print('Access denied: Admin page visited without password.')
        return redirect(url_for('admin_login'))
    topics = Topic.query.all()
    messages = Message.query.all()
    return render_template("admin.html", topics=topics, messages=messages)

@app.errorhandler(404)
def page_not_found(error):
    """Error Page Template"""
    return render_template("404.html"), 404

@app.route("/logout")
def logout():
    """ logout from the admin """
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route("/delete_message/<int:id>")
def delete_message(id):
    """Admin => Deleting messages """
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Find message
    message_to_delete = Message.query.get_or_404(id)

    try:
        # Delete
        db.session.delete(message_to_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while deleting the message...", 500

@app.route("/delete_topic/<int:id>")
def delete_topic(id):
    """ Admin => Deleting topics """
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Find topic
    topic_to_delete = Topic.query.get_or_404(id)

    try:
        # Delete topic and all messages
        db.session.delete(topic_to_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while deleting the topic.", 500

if __name__ == "__main__":
    # creating tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
