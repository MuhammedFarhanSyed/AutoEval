# 🎓 Auto Evaluation System (AutoEval)

An AI-powered automated answer evaluation platform built with **Django** and **Natural Language Processing (NLP)**. The system automatically assesses student descriptive text responses against faculty reference model answers using **NLTK Jaccard Distance** and **Scikit-Learn Cosine Similarity** algorithms, assigning marks out of 100 and automated letter grades (`A`, `B`, `C`, `F`).

---

## 🚀 Features
[deployed on](https://autoeval-87mw.onrender.com)

- 👨‍🎓 **Student Portal**: Account registration, login, interactive exam interface, score overview, and question-by-question result breakdown.
- 👨‍🏫 **Admin / Faculty Portal**: Admin dashboard, student registration approval (`accept`/`decline`), subject creation, and question paper setup with model reference answers.
- 🤖 **Automated NLP Evaluation**:
  - Text tokenization (`nltk.tokenize.word_tokenize`)
  - Case normalization and stop-word filtering (`nltk.corpus.stopwords`)
  - Similarity score calculation using **NLTK Jaccard Distance** and **Scikit-Learn Cosine Similarity** (`CountVectorizer`)
- 📊 **Automatic Grade & Score Generation**: Converts float similarity scores into itemized marks per question ($\text{score} \times 20$) and maps total score out of 100 to letter grades (`A`, `B`, `C`, `F`).
- 📈 **Performance Analytics**: Graphical grade distribution analytics (pie/bar count for grades A, B, C, F).
- 🔒 **Role-Based Authentication & Session Management**: Secure user sessions, account approval workflows, and protected routes.

---

## 🛠️ Tech Stack

### Backend & Web Framework
- **Python 3.10**
- **Django 4.1.6** (Web Framework, ORM, Sessions, Authentication)
- **MySQL** (Database via `mysqlclient 2.1.1`)

### AI & Natural Language Processing (NLP)
- **NLTK 3.8.1**: Tokenization (`word_tokenize`), English Stop Words removal, and Jaccard Distance (`jaccard_distance`).
- **Scikit-Learn 1.2.1**: Bag-of-words vectorization (`CountVectorizer`) and spatial matrix similarity (`cosine_similarity`).
- **NumPy 1.24.2 & SciPy 1.10.0**: Numerical matrix computations.

### Frontend & Media
- **HTML5, CSS3, JavaScript, Bootstrap**
- **SweetAlert**: Interactive alert modals
- **Pillow 9.4.0**: Image handling for user profile photos and subject thumbnails

---

## 📂 Project Structure

```
AutoEval/
│
├── answer_evaluation/          # Django Project Core Configuration
│   ├── settings.py             # Database (MySQL), apps, middleware, media settings
│   ├── urls.py                 # Central URL routing for Admin and User apps
│   ├── asgi.py                 # ASGI entrypoint
│   └── wsgi.py                 # WSGI entrypoint
│
├── adminapp/                   # Admin App (Faculty Portal)
│   ├── models.py               # QuestionModel, SubjectModel
│   ├── views.py                # Subject/question management, user approvals, analytics
│   └── ...
│
├── userapp/                    # User App (Student Portal & NLP Engine)
│   ├── models.py               # UserdetailsModel, AnswerModel, TempModel
│   ├── text_similarity.py      # Core NLP engine (NLTK Jaccard & Sklearn Cosine Similarity)
│   ├── views.py                # Student auth, exam processing, grade assignment
│   └── ...
│
├── assets/                     # Frontend Assets & Layouts
│   ├── templates/              # HTML Templates (admin/ and user/)
│   └── static/                 # Static CSS, JS, Fonts, Images
│
├── media/                      # Uploaded user profile photos & subject images
├── answer_evaluation.sql       # Pre-configured MySQL Database SQL Dump
├── instruction.txt             # Quick deployment instructions
├── req.txt / requirments.txt   # Python package dependencies
├── manage.py                   # Django CLI management tool
└── README.md                   # Project documentation
```

---

## 🤖 NLP Evaluation Workflow & Data Flow

```
+-----------------------------+
| Faculty Uploads Question &  |
| Reference Model Answer      |
+--------------+--------------+
               |
               v
+-----------------------------+
| Student Submits Descriptive |
| Answer Text in Exam Form    |
+--------------+--------------+
               |
               v
+-------------------------------------------------------------+
|                     NLP PROCESSING ENGINE                   |
| 1. Tokenization: nltk.tokenize.word_tokenize(text)           |
| 2. Cleaning: Lowercasing & nltk.corpus.stopwords removal    |
| 3. Math: Jaccard Similarity = 1 - jaccard_distance(set1, set2)|
+--------------+----------------------------------------------+
               |
               v
+-------------------------------------------------------------+
|                   SCORING & GRADE ASSIGNMENT                |
| - Question Mark = int(Similarity * 20) (Max 20 marks/ques)  |
| - Total Score = Sum of 5 questions (Max 100 marks)          |
| - Grade Mapping:                                            |
|   * 76 - 100 -> Grade A                                     |
|   * 50 - 75  -> Grade B                                     |
|   * 25 - 49  -> Grade C                                     |
|   * 0  - 24  -> Grade F                                     |
+--------------+----------------------------------------------+
               |
               v
+-------------------------------------------------------------+
| Saved to AnswerModel DB & Displayed in Student/Admin Dash   |
+-------------------------------------------------------------+
```

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
- **Python 3.10** installed on your system.
- **XAMPP / MySQL Server** installed and running on port `3306`.

---

### 2. Clone the Repository & Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/MuhammedFarhanSyed/AutoEval.git
cd AutoEval

# Create Python 3.10 virtual environment
py -3.10 -m venv myvenv

# Activate virtual environment
# On Windows (PowerShell):
.\myvenv\Scripts\Activate.ps1
# On Linux/Mac:
source myvenv/bin/activate
```

---

### 3. Install Required Dependencies

```bash
pip install -r req.txt
```

---

### 4. Database Setup (MySQL & XAMPP)

1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Open [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/) in your web browser.
3. Click **New** and create a database named:
   ```
   answer_evaluation
   ```
4. Select the `answer_evaluation` database, click the **Import** tab, choose the file [`answer_evaluation.sql`](file:///d:/dummy%20projects/auto-eval/AutoEval/answer_evaluation.sql) from the project root directory, and click **Import**.

---

### 5. Apply Migrations & Start Server

```bash
# Run Django database migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 🔑 Login Credentials

- **Admin Portal**: [http://127.0.0.1:8000/admin-login](http://127.0.0.1:8000/admin-login)
  - **Username**: `admin`
  - **Password**: `admin`
- **Student Portal**: Register a new student account at `/user-register`, then approve the status in the Admin panel under **Pending Registrations**.

---

## 👨‍💻 Author

**Syed Muhammad Farhan**
- GitHub: [https://github.com/MuhammedFarhanSyed](https://github.com/MuhammedFarhanSyed)

---

## 📄 License

This project is open-source and intended for educational and research purposes.
