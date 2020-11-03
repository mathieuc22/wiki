from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django.http import Http404

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    if request.method == "POST":
        t = request.POST['title']
        c = f"# {t} \n \n {request.POST['entry']}"
        e = util.get_entry(t)
        if  e is None:
            util.save_entry(t, c)
            msg = f"entry {t} saved"
        else:
            msg = f"entry {t} already exists"
    else:
        msg = ""
    return render(request, "encyclopedia/new.html", {
        "msg": msg
    })

def entry(request, entry):
    e = util.get_entry(entry)
    if  e is None:
        return render(request, "encyclopedia/404.html", {
        })
    else:
        return render(request, f"encyclopedia/entry.html", {
            "entry": markdowner.convert(e)
        })

def search(request):
    if request.method == "POST":
        q = request.POST['q']
        match = util.get_entry(q)
        if  match is None:
            matching = [s for s in util.list_entries() if q.lower() in s.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": matching
            })
        else:
            return render(request, f"encyclopedia/entry.html", {
                "entry": markdowner.convert(match)
            })
    else:
        return HttpResponseRedirect("/")