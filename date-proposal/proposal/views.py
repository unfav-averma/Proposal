from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import date
from .models import ProposalResponse

# =========================
# HOME PAGE
# =========================

def home(request):
    return render(request, "proposal/index.html")


# =========================
# START PROPOSAL
# =========================

@require_POST
def start_proposal(request):

    # Start a new proposal session
    request.session["proposal_started"] = True

    # Make sure old selections are removed
    request.session.pop("date_type_selected", None)
    request.session.pop("selected_date", None)
    request.session.pop("selected_time", None)
    request.session.pop("proposal_response_id", None)

    return JsonResponse({"success": True})


# =========================
# DATE TYPE PAGE
# =========================

def date_page(request):

    # User must click YES first
    if not request.session.get("proposal_started"):
        return redirect("home")

    return render(request, "proposal/date.html")


# =========================
# SELECT DATE PAGE
# =========================

def select_date(request):

    # User must have selected a date type
    if not request.session.get("date_type_selected"):
        return redirect("date_page")

    return render(request, "proposal/select_date.html")


# =========================
# THANK YOU PAGE
# =========================

def thank_you(request):

    # Get the database record created during final selection
    response_id = request.session.get("proposal_response_id")

    if not response_id:
        return redirect("select_date")

    try:
        response = ProposalResponse.objects.get(id=response_id)

    except ProposalResponse.DoesNotExist:
        return redirect("select_date")

    return render(
        request,
        "proposal/thank_you.html",
        {
            "response": response
        }
    )

@require_POST
def save_date_type(request):

    if not request.session.get("proposal_started"):
        return JsonResponse({
            "success": False,
            "error": "Proposal has not been started."
        }, status=400)

    try:
        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise TypeError

        date_type = data.get("date_type")
        if isinstance(date_type, str):
            date_type = date_type.strip()

        if not date_type:
            return JsonResponse({
                "success": False
            }, status=400)

        request.session["date_type_selected"] = date_type

        return JsonResponse({
            "success": True
        })

    except (json.JSONDecodeError, TypeError, UnicodeDecodeError):

        return JsonResponse({
            "success": False
        }, status=400)

@require_POST
def save_selection(request):

    # User must have selected a date type first
    date_type = request.session.get("date_type_selected")

    if not date_type:
        return JsonResponse({
            "success": False,
            "error": "Date type not selected."
        }, status=400)

    try:

        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise TypeError

        selected_date = data.get("selected_date")
        selected_time = data.get("selected_time")

        if isinstance(selected_date, str):
            selected_date = selected_date.strip()
        if isinstance(selected_time, str):
            selected_time = selected_time.strip()

        if not selected_date or not selected_time:
            return JsonResponse({
                "success": False,
                "error": "Date and time are required."
            }, status=400)

        # Convert YYYY-MM-DD string into a Python date
        selected_date_object = date.fromisoformat(selected_date)

        # Save permanently in database
        response = ProposalResponse.objects.create(
            date_type=date_type,
            selected_date=selected_date_object,
            selected_time=selected_time
        )

        # Also keep the information in the current session
        request.session["selected_date"] = selected_date
        request.session["selected_time"] = selected_time

        # Remember which database record belongs to this session
        request.session["proposal_response_id"] = response.id

        return JsonResponse({
            "success": True
        })

    except (json.JSONDecodeError, TypeError, UnicodeDecodeError, ValueError):

        return JsonResponse({
            "success": False,
            "error": "Invalid date or data."
        }, status=400)