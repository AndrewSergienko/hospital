from django.shortcuts import render, redirect

from account.forms import EditUserForm
from actions.models import Action


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            request.user.full_name = form.cleaned_data['full_name']
            request.user.email = form.cleaned_data['email']
            request.user.specialty = form.cleaned_data['speciality']
            request.user.save()
    edit_form = EditUserForm()
    edit_form.fields['full_name'].initial = request.user.full_name
    edit_form.fields['email'].initial = request.user.email
    edit_form.fields['speciality'].initial = request.user.specialty or "Невідомо"
    actions = Action.objects.order_by("-id")[:10]
    context = {
        'user': request.user,
        'edit_form': edit_form,
        'actions': actions
    }
    return render(request, 'dashboard.html', context)
