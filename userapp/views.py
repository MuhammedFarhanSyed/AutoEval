import ast
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import QuestionModel, SubjectModel
from userapp.models import UserdetailsModel, AnswerModel, TempModel
from userapp.text_similarity import text_similarity_nltk

# ==============================================================================
# USER & AUTHENTICATION VIEWS MODULE
# ==============================================================================

def index(request):
    """
    Renders the public landing / home page of the website.
    """
    return render(request, "user/index.html")


def admin_login(request):
    """
    Handles administrator authentication.
    Checks fixed admin credentials ('admin' / 'admin') and redirects to Admin Dashboard upon success.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "admin":
            messages.success(request, "Logged In Successfully.")
            return redirect('admin_index')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('admin_login')
            
    return render(request, "admin/admin-login.html")


def user_login(request):
    """
    Handles student user login authentication and account status checks.
    
    Status checks:
      - 'accepted': Sets session 'user_id' and redirects to Student Dashboard.
      - 'pending': Warns user that registration is awaiting admin approval.
      - 'blocked': Prevents access due to account blocking.
    """
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        try:
            auth = UserdetailsModel.objects.get(user_email=username, user_password=password)
            if auth.user_status == "accepted":
                request.session['user_id'] = auth.user_id
                messages.success(request, 'Successfully Logged In')
                return redirect('user_dashboard')
            elif auth.user_status == "pending":
                messages.info(request, 'Your id is pending for registration approval.')
                return redirect('user_login')
            elif auth.user_status == "blocked":
                messages.error(request, 'You are BLOCKED from logging in.')
                return redirect('user_login')
            else:
                messages.error(request, 'You are not registered, try again after signup.')
                return redirect('user_login')
            
        except UserdetailsModel.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
            return redirect('user_login')
            
    return render(request, "user/user-login.html")


def user_register(request):
    """
    Handles student registration account creation.
    Checks if email already exists before storing user profile and photo.
    Initial user status is set to 'pending' awaiting admin approval.
    """
    if request.method == "POST" and request.FILES.get("photo"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        student_id = request.POST.get('id')
        photo = request.FILES['photo']

        try:
            UserdetailsModel.objects.get(user_email=email)
            messages.info(request, "Email already exists, try again with another email.")
            return redirect('user_register')
        except UserdetailsModel.DoesNotExist:
            user_create = UserdetailsModel.objects.create(
                user_name=name,
                user_email=email,
                user_password=password,
                user_contact=contact,
                student_id=student_id,
                user_photo=photo
            )
            
            if user_create:
                messages.success(request, "Successfully Registered. Please wait for admin approval.")
                return redirect('user_register')
            else:
                messages.error(request, "Invalid details, try again.")
                return redirect('user_register')
                
    return render(request, "user/user-register.html")


def user_contact(request):
    """
    Renders the public contact page.
    """
    return render(request, "user/user-contact.html")


def user_dashboard(request):
    """
    Renders the logged-in student's dashboard showing summary statistics:
    - Number of exams completed
    - Number of unique subjects attempted
    - Total questions answered
    """
    user_id = request.session['user_id']
    exams_count = AnswerModel.objects.filter(user_id=user_id).count()
    exams = AnswerModel.objects.filter(user_id=user_id)
    
    # Calculate unique subjects attempted
    sub = []
    for i in exams:
        if i.answer_subject not in sub:
            sub.append(i.answer_subject)
            
    ques_count = exams_count * 5
    subjects_count = len(sub)
    return render(request, "user/user-dashboard.html", {
        'exams': exams_count,
        'subjects': subjects_count,
        'ques': ques_count
    })


def user_questions(request, subject):
    """
    Core Evaluation Engine Function:
    1. Displays the 5 questions for a given subject.
    2. Receives student's submitted text answers via POST.
    3. Runs NLTK NLP similarity (text_similarity_nltk) against model answers.
    4. Computes marks out of 20 per question (Total score out of 100).
    5. Assigns letter grades (A: 76-100, B: 50-75, C: 25-49, F: 0-24).
    6. Saves submission details to AnswerModel.
    """
    user_id = request.session['user_id']
    user = UserdetailsModel.objects.get(user_id=user_id)
    sub = QuestionModel.objects.filter(subject=subject)

    if request.method == 'POST':
        # Retrieve 5 student answers from form submission
        q1 = request.POST.get('question1')
        q2 = request.POST.get('question3')
        q3 = request.POST.get('question4')
        q4 = request.POST.get('question5')
        q5 = request.POST.get('question6')

        # Compute NLTK NLP similarity score (0.0 to 1.0) and multiply by 20 marks
        r1 = int((text_similarity_nltk(q1, sub[0].answer)) * 20)
        r2 = int((text_similarity_nltk(q2, sub[1].answer)) * 20)
        r3 = int((text_similarity_nltk(q3, sub[2].answer)) * 20)
        r4 = int((text_similarity_nltk(q4, sub[3].answer)) * 20)
        r5 = int((text_similarity_nltk(q5, sub[4].answer)) * 20)

        # Total score out of 100
        score = r1 + r2 + r3 + r4 + r5
        
        # Determine final letter grade
        if score <= 24:
            grade = 'F'
        elif 25 <= score <= 49:
            grade = 'C'
        elif 50 <= score <= 75:
            grade = 'B'
        elif 76 <= score <= 100:
            grade = 'A'

        # Package questions, student answers, and individual marks into dictionary
        answer_dict = {
            'question1': {'question': sub[0].question, 'answer': q1, 'marks': str(r1)},
            'question2': {'question': sub[1].question, 'answer': q2, 'marks': str(r2)},
            'question3': {'question': sub[2].question, 'answer': q3, 'marks': str(r3)},
            'question4': {'question': sub[3].question, 'answer': q4, 'marks': str(r4)},
            'question5': {'question': sub[4].question, 'answer': q5, 'marks': str(r5)}
        }

        # Save result into database
        AnswerModel.objects.create(
            answer_subject=subject,
            answer=answer_dict,
            user_id=user,
            score=score,
            grade=grade
        )

        messages.success(request, "Answers submitted and evaluated successfully!")
        return redirect("user_exam")
        
    try:
        # Render the 5 questions on the exam page
        return render(request, "user/user-questions.html", {
            'quest1': sub[0],
            'quest2': sub[1],
            'quest3': sub[2],
            'quest4': sub[3],
            'quest5': sub[4],
        })
    except IndexError:
        messages.error(request, "Something Went Wrong. Ensure 5 questions are added by admin for this subject.")
        return redirect("user_exam")


def user_view_results(request, answer_id):
    """
    Unpacks stored dictionary string of an exam result into TempModel table
    to display a detailed question-by-question marks breakdown.
    """
    TempModel.objects.all().delete()  # Clear temporary table
    result = AnswerModel.objects.get(answer_id=answer_id)
    answer_dict = ast.literal_eval(result.answer)
    
    # Populate temp model with individual question evaluation data
    for key, value in answer_dict.items():
        TempModel.objects.create(
            subject=result.answer_subject,
            question=value['question'],
            answer=value['answer'],
            score=value['marks']
        )
        
    f_results = TempModel.objects.all()
    return render(request, "user/user-view-results.html", {'result': f_results})


def user_results(request):
    """
    Displays historical exam results submitted by the currently logged-in student.
    """
    user_id = request.session['user_id']
    result = AnswerModel.objects.filter(user_id=user_id)
    return render(request, "user/user-results.html", {'result': result})


def user_myprofile(request):
    """
    Allows the logged-in student to view and update their profile details and photo.
    """
    user_id = request.session['user_id']
    user = UserdetailsModel.objects.get(user_id=user_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        contact = request.POST.get("contact")
        student_id = request.POST.get("id")
        
        user.user_name = name
        user.user_email = email
        user.user_password = password
        user.user_contact = contact
        user.student_id = student_id
        
        if request.FILES.get('photo'):
            user.user_photo = request.FILES['photo']

        user.save()
        messages.success(request, "Successfully Updated Profile")
        return redirect("user_myprofile")

    return render(request, "user/user-myprofile.html", {'user': user})


def user_exam(request):
    """
    Displays list of available subject cards so students can select an exam to take.
    """
    sub = SubjectModel.objects.all()
    return render(request, "user/user-exam.html", {'sub': sub})








def user_results(request):
    user_id=request.session['user_id']

    result = AnswerModel.objects.filter(user_id = user_id)
    return render(request,"user/user-results.html",{'result':result})

def user_myprofile(request):
    user_id=request.session['user_id']
    user=UserdetailsModel.objects.get(user_id=user_id)

    
    if request.method=="POST":
        if len(request.FILES) ==0:
            name=request.POST.get("name")
            
            email=request.POST.get("email")
            password=request.POST.get("password")
            contact=request.POST.get("contact")
            id = request.POST.get("id")
            
            user.user_name = name
            
            user.user_email = email
            user.user_password = password
            user.user_contact = contact
            user.student_id =  id
            

            user.save()
            if user:
                messages.success(request,"Succesflly Updated")
                return redirect("user_myprofile")

            else:
                messages.error(request,"No changes detected")
                return redirect("user_myprofile")
    else:
        if request.method=="POST" and request.FILES['photo']:
            name=request.POST.get("name")
        
            email=request.POST.get("email")
            password=request.POST.get("password")
            contact=request.POST.get("contact")
            id = request.POST.get("id")
            
            photo=request.FILES["photo"]
            user.user_name = name
            
            user.user_email = email
            user.user_password = password
            user.user_contact = contact
            user.student_id =  id
            user.user_photo = photo
            
            

            user.save()
            if user:
                messages.success(request,"Succesflly Updated")
                return redirect("user_myprofile")
            

                

            else:
                messages.error(request,"No changes detected")
                return redirect("user_myprofile")
    return render(request,"user/user-myprofile.html",{'user':user})

def user_exam(request):
    sub = SubjectModel.objects.all()

    return render(request,"user/user-exam.html",{'sub':sub})