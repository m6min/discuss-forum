# 🚀 Discuss | Minimalist Forum with Flask

**Discuss** is a lightweight, responsive, and secure forum application built with **Flask** and **SQLAlchemy**. Designed for simplicity and speed, it features a custom **CSS Grid** layout and a robust administrative backend.

---

## ✨ Features

* **Threaded Discussions:** Create new topics and reply with ease.
* **Search Functionality:** Instant search through topics using `SQLAlchemy` filters.
* **Admin Control Center:**
    * Secure login with **Session management**.
    * Delete inappropriate **topics** or **messages**.
    * Track **IP Addresses** of all users for moderation.
* **Responsive UI:** A custom-built **CSS Grid** system that works on mobile and desktop without external libraries.
* **Safe Deletion:** Uses `Cascade Delete` to ensure database integrity when removing topics.

---

## 🛠️ Tech Stack

| Tool | Purpose |
| :--- | :--- |
| **Python** | Logic & Backend |
| **Flask** | Web Framework |
| **SQLAlchemy** | Database Management (ORM) |
| **Dotenv** | Secret Management (.env) |
| **Jinja2** | Template Engine |

---

## 🚀 Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the repository
```bash
git clone https://github.com/m6min/discuss-forum.git
cd discuss-forum
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root folder and add your secrets:
```env
SECRET_KEY=your_very_secret_key_here
ADMIN_PASSWORD=your_admin_password_here
```

### 5. Run the Application
```bash
python app.py
```

**Note:** The database (`forum.db`) will be automatically created on the first run.

Visit **http://127.0.0.1:5000** to see the app.

---

## 📂 Project Structure
```
discuss/
├── app.py                 # Main application file
├── templates/             # HTML templates (Jinja2)
├── static/                # CSS, JS, images
├── forum.db               # SQLite database (auto-generated)
├── .env                   # Environment variables (not in repo)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🔐 Admin Panel

Access the admin panel at `/admin` to:
- View all topics and messages
- Delete inappropriate content
- Monitor user IP addresses for moderation

**Default Login:** Use the `ADMIN_PASSWORD` you set in the `.env` file.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Mümin Filiz**
- GitHub: [m6min](https://github.com/m6min)

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!