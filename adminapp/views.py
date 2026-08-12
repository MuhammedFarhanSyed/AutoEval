from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from adminapp.models import QuestionModel, SubjectModel
from userapp.models import UserdetailsModel, AnswerModel

# ==============================================================================
# ADMIN VIEWS MODULE
# ==============================================================================

def admin_index(request):
    """
    Renders the main Admin Dashboard overview.
    Counts pending users, registered users, uploaded questions, and total answers.
    """
    pend = UserdetailsModel.objects.filter(user_status="pending").count()
    all_users = UserdetailsModel.objects.all().count()
    ques = QuestionModel.objects.all().count()
    ans = AnswerModel.objects.all().count()
    return render(request, "admin/admin-index.html", {
        'ques': ques,
        'all': all_users,
        'ans': ans,
        'pend': pend
    })


def admin_pending(request):
    """
    Displays a paginated list of student registrations pending admin approval.
    """
    pending = UserdetailsModel.objects.filter(user_status="pending")
    paginator = Paginator(pending, 5)  # Show 5 records per page
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request, "admin/admin-pending.html", {'pend': page})


def admin_all(request):
    """
    Displays a paginated list of all registered student accounts.
    """
    all_users = UserdetailsModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request, "admin/admin-all.html", {'all': page})


def admin_add_subject(request):
    """
    Allows the admin to add a new academic subject along with a thumbnail photo.
    Checks if subject already exists to prevent duplicate entries.
    """
    sub = SubjectModel.objects.all()
    if request.method == "POST" and request.FILES.get('photo'):
        subject = request.POST.get('subject')
        photo = request.FILES['photo']

        try:
            SubjectModel.objects.get(subject=subject.lower())
            messages.error(request, "This subject already exists, Try another subject")
            return redirect('admin_add_subject')
        except SubjectModel.DoesNotExist:
            SubjectModel.objects.create(subject=subject.lower(), subject_image=photo)
            messages.success(request, f"{subject} subject added successfully")
            return redirect('admin_add_subject')
            
    return render(request, "admin/admin-add-subject.html", {'sub': sub})


def admin_add_question(request):
    """
    Allows admin to upload a question and its reference model answer for a subject.
    Enforces a maximum limit of 5 questions per subject.
    """
    sub = SubjectModel.objects.all()
    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        subject = request.POST.get('subject')
        
        # Ensure max limit of 5 questions per subject (index 0 to 4)
        if QuestionModel.objects.filter(subject=subject).count() <= 4:
            QuestionModel.objects.create(question=question, answer=answer, subject=subject)
            messages.success(request, "Question added successfully")
            return redirect('admin_add_question')
        else:
            messages.info(request, f"Limit reached for questions in {subject}. Remove a question to add a new one.")
            return redirect('admin_add_question')
            
    return render(request, "admin/admin-add-question.html", {'sub': sub})


def admin_manage_question(request):
    """
    Displays a paginated table of all questions and model answers for editing/deleting.
    """
    ques = QuestionModel.objects.all()
    paginator = Paginator(ques, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request, "admin/admin-manage-question.html", {'ques': page})


def admin_results(request):
    """
    Displays a paginated list of all student exam evaluation results.
    """
    result = AnswerModel.objects.all()
    paginator = Paginator(result, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request, "admin/admin-results.html", {'result': page})


def admin_analysis_graph(request):
    """
    Calculates grade distribution counts (A, B, C, F) for performance analytics charts.
    """
    f = AnswerModel.objects.filter(grade='F').count()
    c = AnswerModel.objects.filter(grade='C').count()
    b = AnswerModel.objects.filter(grade='B').count()
    a = AnswerModel.objects.filter(grade='A').count()

    return render(request, "admin/admin-analysis-graph.html", {'a': a, 'b': b, 'c': c, 'f': f})


def accept_user(request, user_id):
    """
    Approves a pending student registration request by updating user_status to 'accepted'.
    """
    accept = get_object_or_404(UserdetailsModel, user_id=user_id)
    accept.user_status = "accepted"
    accept.save()
    messages.success(request, "User Approved Successfully")
    return redirect('admin_pending')


def decline_user(request, user_id):
    """
    Rejects a pending student registration request by updating user_status to 'declined'.
    """
    decline = get_object_or_404(UserdetailsModel, user_id=user_id)
    decline.user_status = "declined"
    decline.save()
    messages.success(request, "User Rejected Successfully")
    return redirect('admin_pending')


def remove_questions(request, question_id):
    """
    Deletes a specific question and reference answer from the database.
    """
    get_object_or_404(QuestionModel, question_id=question_id).delete()
    messages.success(request, "Question Removed Successfully")
    return redirect('admin_manage_question')


def remove_subject(request, subject_id):
    """
    Deletes a subject entry from the database.
    """
    get_object_or_404(SubjectModel, subject_id=subject_id).delete()
    messages.success(request, "Subject Removed Successfully")
    return redirect('admin_add_subject')