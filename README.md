# 🎓 Auto Evaluation System

An AI-powered answer evaluation system built with **Django** that automates the assessment of descriptive answers using Natural Language Processing (NLP) techniques. The platform helps educators evaluate student responses quickly, consistently, and accurately while reducing manual effort.

---

## 🚀 Features

- 👨‍🎓 Student Registration & Login
- 👨‍🏫 Faculty/Admin Dashboard
- 📄 Upload Question Papers
- 📝 Student Answer Submission
- 🤖 AI-Based Answer Evaluation
- 📊 Automatic Score Generation
- 📈 Result Dashboard
- 📋 Evaluation History
- 🔒 Secure Authentication
- 📱 Responsive Web Interface

---

## 🛠️ Tech Stack

### Backend
- Django
- Python 3.x
- Django ORM

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Database
- MySQL

### AI/NLP
- Sentence Transformers
- FAISS (Vector Search)
- LangChain
- Groq LLM API

---

## 📂 Project Structure

```
auto_evaluation/
│
├── answer_evaluation/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── ...
│
├── media/
├── static/
├── db.sqlite3 / MySQL
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/auto-evaluation-system.git

cd auto-evaluation-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Database

Update your `settings.py` with your MySQL credentials.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "database_name",
        "USER": "username",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

---

### 5. Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7. Run the Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 🤖 AI Evaluation Workflow

1. Faculty uploads the model answer.
2. Student submits their answer.
3. Text is converted into embeddings.
4. Similarity is calculated using FAISS.
5. LangChain retrieves relevant context.
6. Groq LLM evaluates the answer.
7. Marks and feedback are generated automatically.

---

## 📸 Screenshots

Add screenshots here.

```
Home Page

Student Dashboard

Faculty Dashboard

Evaluation Result
```

---

## 📦 Requirements

Example dependencies:

```
Django
mysqlclient
langchain
langchain-community
langchain-groq
sentence-transformers
faiss-cpu
numpy
torch
python-dotenv
```

Generate automatically:

```bash
pip freeze > requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key

SECRET_KEY=your_django_secret_key

DEBUG=True
```

---

## 📈 Future Improvements

- PDF Answer Evaluation
- OCR for Handwritten Answers
- Multi-language Support
- Question Difficulty Analysis
- Plagiarism Detection
- Teacher Feedback Suggestions
- Analytics Dashboard
- REST API Integration

---

## 👨‍💻 Author

**Syed Muhammad Farhan**

- GitHub: https://github.com/MuhammedFarhanSyed
- LinkedIn: https://www.linkedin.com/in/muhammed-farhan-syed

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and research purposes.
