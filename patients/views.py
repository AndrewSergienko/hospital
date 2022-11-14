import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from actions.models import Action
from patients.forms import AddCardForm, AddNoteForm
from patients.models import PatientCard, ExaminationNote


@login_required
def card_list(request):
    queryset = ""
    search = 'search-input' in request.GET
    filters = 'filter-date-1' in request.GET or 'filter-date-2' in request.GET
    if search:
        queryset = PatientCard.objects.filter(full_name__contains=request.GET['search-input'])
    if filters:
        queryset = filter_cards(
            request.GET['filter-date-1'] if 'filter-date-1' in request.GET else None,
            request.GET['filter-date-2'] if 'filter-date-2' in request.GET else None,
            queryset if 'search-input' in request.GET else None
        )
    if 'sort-date' in request.GET:
        if request.GET['sort-date'] == "down":
            queryset = queryset.order_by('-date_of_birth') if search or filters else PatientCard.objects.order_by('-date_of_birth')
        else:
            queryset = queryset.order_by(
                'date_of_birth') if search or filters else PatientCard.objects.order_by('date_of_birth')
    queryset = queryset if queryset else PatientCard.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET['page'] if 'page' in request.GET else 1
    page_obj = paginator.get_page(page_number)
    form = AddCardForm()
    return render(request, 'patients/list.html', {'page_obj': page_obj, 'form': form})


def filter_cards(date1, date2, queryset=None):
    if queryset:
        if date1 and date2:
            return queryset.filter(date_of_birth__range=[date1, date2])
        elif date1:
            return queryset.filter(date_of_birth__gte=date1)
        else:
            return queryset.filter(date_of_birth__lte=date2)
    else:
        if date1 and date2:
            return PatientCard.objects.filter(date_of_birth__range=[date1, date2])
        elif date1:
            return PatientCard.objects.filter(date_of_birth__gte=date1)
        else:
            return PatientCard.objects.filter(date_of_birth__lte=date2)


@login_required
def add_card(request):
    if request.method == "POST":
        form = AddCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.save()
            create_action(request.user, "створив карту:", card)
            return redirect('patients:card_list')
        else:
            return HttpResponse("Error")
    return HttpResponse("Ezzz")


@login_required
def add_note(request, card_id):
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            card = PatientCard.objects.get(id=card_id)
            note.card = card
            note.doctor = request.user
            note.save()
            create_action(request.user, "добавив запис в карті:", card)
            return redirect('patients:card_info', card_id)
        else:
            return HttpResponse("Error")
    form = AddNoteForm()
    return render(request, "patients/addNote.html", {'form': form})


@login_required
def card_info(request, card_id):
    card = PatientCard.objects.get(id=card_id)
    notes_queryset = card.examination_notes.order_by("-id")
    notes_paginator = Paginator(notes_queryset, 10)
    page = request.GET['notes_page'] if 'notes_page' in request.GET else 1
    notes = notes_paginator.get_page(page)
    form_add_note = AddNoteForm()
    form_edit_info = AddCardForm()
    form_edit_info.fields['full_name'].initial = card.full_name
    form_edit_info.fields['date_of_birth'].initial = card.date_of_birth
    form_edit_info.fields['home_address'].initial = card.home_address
    form_edit_note = AddNoteForm()
    context = {
        "card": card,
        "notes": notes,
        "form_add_note": form_add_note,
        "form_edit_info": form_edit_info,
        "form_edit_note": form_edit_note
    }
    return render(request, "patients/cardInfo.html", context)


@login_required
def edit_card_info(request, card_id):
    if request.method == 'POST':
        form = AddCardForm(request.POST)
        if form.is_valid():
            card = PatientCard.objects.get(id=card_id)
            edited_card = form.save(commit=False)
            card.full_name = edited_card.full_name
            card.date_of_birth = edited_card.date_of_birth
            card.home_address = edited_card.home_address
            card.save()
            create_action(request.user, "змінив інформацію про карту:", card)
            content = {
                'full_name': card.full_name,
                'date_of_birth': card.date_of_birth.strftime('%d.%m.%Y'),
                'home_address': card.home_address
            }
            return HttpResponse(json.dumps(content), content_type="application/json")
    return HttpResponse(status=400)


@login_required
def card_delete(request, card_id):
    card = PatientCard.objects.get(id=card_id)
    create_action(request.user, "видалив карту:", target_name=card.full_name)
    card.delete()
    return redirect("patients:card_list")


@login_required
def edit_note(request, note_id):
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            edited_note = form.save(commit=False)
            note = ExaminationNote.objects.get(id=note_id)
            note.text = edited_note.text
            create_action(request.user, "змінив запис в карті:", note.card)
            note.save()
            return HttpResponse(json.dumps({'text': note.text}), content_type="application/json")
    return HttpResponse(status=400)


@login_required
def delete_note(request, note_id):
    note = ExaminationNote.objects.get(id=note_id)
    card_id = note.card.id
    create_action(request.user, 'видалив запис в карті:', note.card)
    note.delete()
    return redirect("patients:card_info", card_id)


def create_action(author, action_text, target=None, target_name=None):
    Action(
        author=author,
        author_name=author.full_name,
        target=target,
        target_name=target_name if target_name else target.full_name,
        action_text=action_text
    ).save()