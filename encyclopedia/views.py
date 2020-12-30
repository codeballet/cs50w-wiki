import markdown2
import re

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


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


def entry(request, title):
    md_text = util.get_entry(title)

    if md_text == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "title": title.upper(),
        "text": markdown2.markdown(md_text)
    })
