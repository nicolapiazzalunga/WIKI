from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import markdown2
import random

from . import util

# Sets a class inheriting from django forms for the forms in new_entry and edit_entry
class NewEntryForm(forms.Form):

    entry_title = forms.CharField(
        label="Entry Title",
        widget=forms.TextInput(attrs={'placeholder': 'New Entry'})
        )

    entry_text = forms.CharField(
        label="Entry Text",
        widget=forms.Textarea(attrs={
            'placeholder': 'Entry Text', 
            'style': 'height: 400px; width: 700px'
            })
        )
        

def index(request):
    
    if request.method == "POST":

        entry_name = request.POST["q"]
        list_of_entries = util.list_entries()

        # Tests if en entry exists
        if entry_name.upper() in [x.upper() for x in list_of_entries]:
            return redirect(
                "entry",
                entry_name = entry_name
            )
        else:
            partial_matches = []

            for entry in list_of_entries:
                if entry_name.upper() in entry.upper():
                    partial_matches += [entry]

            if len(partial_matches) == 0:
                # Set a redirect in the more verbose way
                return HttpResponseRedirect(reverse(
                    "entry",
                    kwargs={'entry_name': "missing entry"}
                ))
            else:
                request.session["partial_matches"] = partial_matches
                # Set a redirect using the redirect shortcut
                return redirect("search_results")

    # If request method is GET
    request.session["partial_matches"] = []
    entries = util.list_entries()
    entries.sort()

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, entry_name):

    if entry_name == "missing entry":
        return render(request, "encyclopedia/entry.html", {
        "entry_missing": True
    })
    else:
        entry_text = util.get_entry(entry_name)
        entry_name = entry_name.upper()

        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry_name,
            "entry_text": markdown2.markdown(entry_text)
        })


def search_results(request):

    return render(request, "encyclopedia/search_results.html", {
        "partial_matches": request.session["partial_matches"]
    })


def new_entry(request):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():

            entry_title = form.cleaned_data["entry_title"]
            if entry_title.upper() in [x.upper() for x in util.list_entries()]:
                return render(request, "encyclopedia/new_entry.html", {
                    "entry_exists": True
                })
            else:
                entry_text = form.cleaned_data["entry_text"]
                util.save_entry(entry_title, entry_text)

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm()
    })


def edit_entry(request, entry_name):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_text = form.cleaned_data["entry_text"]
            util.save_entry(entry_name, entry_text)
            return redirect("entry", entry_name=entry_name)
        else:
            return HttpResponse("nope")

    entry_text = util.get_entry(entry_name)
    form = NewEntryForm(initial={
        'entry_title': entry_name,
        'entry_text': entry_text
        })

    return render(request, "encyclopedia/edit_entry.html", {
        "form": form,
        'entry_name': entry_name
    })


def random_entry(request):

    list_entries = util.list_entries()
    random_entry = random.choice(list_entries)

    return redirect("entry", entry_name=random_entry)