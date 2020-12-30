import markdown2
import re

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(max_length=250)

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title", min_length=1, max_length=250, strip=True)
    content = forms.CharField(widget=forms.Textarea, label="Content", min_length=1, max_length=25000, strip=True)


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


def entry(request, title):
    md_text = util.get_entry(title)

    if md_text == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "title": title.upper(),
        "text": markdown2.markdown(md_text)
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