import logging
from urllib.request import Request

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Note

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def index(request: Request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        user = request.user
        notes = Note.objects.filter(user=user)
    else:
        notes = ""
    return render(request, "index.html", {"notes": notes})


@require_http_methods(["POST"])
def handle_user_signup(request: Request):
    """
    Signup to create the user in the system
    :param request:
    :return:
    """
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    _password = request.POST["_password"]

    if User.objects.filter(username=username).first():
        messages.error(request, "This username already exists")
        logger.error("This username already exists")
        return redirect("/")

    if not str(username).isalnum():
        messages.error(request, "Username should contain both alphabets and numbers")
        return redirect("/")

    if str(username).isnumeric():
        messages.error(request, "Username must not contain only numbers")
        return redirect("/")

    if len(username) > 12:
        messages.error(request, "Username should be under 12 characters")
        return redirect("/")

    if str(password).isnumeric():
        messages.error(request, "Password should not contain only numbers")
        return redirect("/")

    if len(password) < 6:
        messages.error(request, "Password should contain atleast 8 characters")
        return redirect("/")

    if password != _password:
        messages.error(request, "Both the password fields should match")
        return redirect("/")

    user = User.objects.create_user(username, email, password)
    user.save()
    messages.success(request, "Your account has been successfully created")
    return redirect("/")


@require_http_methods(["POST"])
def handle_user_login(request: Request):
    """
    Login view to get user authenticated to the system
    :param request:
    :return:
    """
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "You have been successfully logged in")
        logger.info("successfully logged in")
        return redirect("/")
    else:
        messages.error(request, "Invalid Credentials! Please try again")
        return redirect("/")


@require_http_methods(["GET"])
def handle_user_logout(request: Request):
    """
    Logout view for signing off user from the system
    :param request:
    :return:
    """
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect("/")


@require_http_methods(["POST"])
def add_note(request: Request):
    """
    Add view for notes add notes endpoint
    :param request: user sends an edit request with the valid payload
    :return:
    """
    title = request.POST["notestitle"]
    body = request.POST["notesbody"]
    tag = request.POST["notestag"]
    user = request.user

    if len(title) < 6 or len(body) < 8:
        messages.error(
            request,
            "Please keep title and body more than 6 character and 8 char respectively",
        )
        return redirect("/")
    else:
        note = Note(title=title, tag=tag, body=body, user=user)
        note.save()
        messages.success(request, "Your note has been added successfully")
        return redirect("/")


@require_http_methods(["GET"])
def search_note(request: Request, tag: str):
    """
    Search view for notes search notes endpoint
    :param request: user sends an edit request with the valid note id
    :param tag:
    :return:
    """
    if request.user.is_authenticated:
        user = request.user
        # gives latest updated notes with tag
        try:
            note = Note.objects.filter(tag__regex=tag, user_id=user.id).latest()
            if not user == note.user:
                messages.error(request, "Getting other user's notes is forbidden")
                return redirect("/")
        except Note.DoesNotExist:
            messages.error(request, "Notes not present with the tag id")
            return redirect("/")
        else:
            messages.success(request, "Please find the latest note with the tag")
            return redirect("/")
    else:
        messages.info(request, "User not authenticated")
        return redirect("/")


@require_http_methods(["GET", "POST"])
def edit_note(request, note_id):
    """
    Edit view for notes edit notes endpoint
    :param request: user sends an edit request with the valid note id
    :param note_id: str
    :return: get rendered an edit view
    """
    if request.user.is_authenticated:
        user = request.user
        note = Note.objects.filter(id=note_id).first()

        if not user == note.user:
            messages.error(request, "Editing other user's notes is forbidden")
            return redirect("/")
        else:
            return render(request, "edit.html", {"note": note})
    else:
        return redirect("/")


@require_http_methods(["POST"])
def update_note(request: Request, note_id: str):
    """
    Update view for notes Update notes endpoint
    :param request: user sends an update request with the valid note id
    :param note_id:
    :payload tile, tag and body of notes
    :return:
    """
    note = Note.objects.filter(id=note_id).first()
    title = request.POST["notestitle"]
    tag = request.POST["notestag"]
    body = request.POST["notesbody"]

    if len(title) < 6 or len(body) < 8:
        messages.error(request, "Please fill the form correctly")
        return redirect(f"/edit/note/{note.id}")
    else:
        note.title = title
        note.tag = tag
        note.body = body
        note.save()
        messages.success(request, "Your note has been updated successfully")
        return redirect(f"/edit/note/{note.id}")


@require_http_methods(["GET", "DELETE"])
def delete_note(request: Request, note_id: str):
    """
    Delete view for the notes delete endpoint
    :param request: user sends a delete request with the valid note id
    :param note_id: str
    :return:
    """
    if request.user.is_authenticated:
        user = request.user
        note = Note.objects.filter(id=note_id).first()

        if (
            not user == note.user
        ):  # check if the loggedin user matches the note user, else forbid the loggedin user to delete other user's note. This line is very much important.
            messages.error(request, "Deleting other user's notes is forbidden")
            return redirect("/")
        else:
            note.delete()
            messages.success(request, "Your note has been deleted successfully")
            return redirect("/")
    else:
        return redirect("/")
