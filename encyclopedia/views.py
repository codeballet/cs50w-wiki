import markdown2
import re

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class EditEntryForm(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea, label="Content", min_length=1, max_length=25000, strip=True)

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title", min_length=1, max_length=250, strip=True)
    content = forms.CharField(widget=forms.Textarea, label="Content", min_length=1, max_length=25000, strip=True)

class SearchForm(forms.Form):
    q = forms.CharField(max_length=250)


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"].lower()
            print(f"Search term: {q}")

            if util.get_entry(q):
                return HttpResponseRedirect(reverse("entry", args=[q]))

            entries_list = util.list_entries()
            matches = []
            for entry in entries_list:
                if re.search(".*" + q + ".*", entry.lower()):
                    matches.append(entry)

            return render(request, "encyclopedia/results.html", {
                "matches": matches
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["edit_content"]
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("entry", args=[title]))

    md_content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(),
        "title": title,
        "content": md_content
    })


def entry(request, title):
    md_content = util.get_entry(title)

    if md_content == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(md_content)
    })

def new(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        
        if form.is_valid():
            entries_list = util.list_entries()
            title = form.cleaned_data["title"].lower()
            content = form.cleaned_data["content"]

            if title in entries_list:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": "Error: That Page already exists! Please choose another Title."
                })

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/new.html", {
        "form": CreateEntryForm()
    })