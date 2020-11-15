from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# import markdown2 for html conversion
from markdown2 import Markdown
from django.http import Http404

from . import util

# import random function
import random

markdowner = Markdown()

def index(request):
    # return a list of all the entries on the index page
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    # if post request handle the new page form
    if request.method == "POST":
        # get the title
        t = request.POST['title']
        # check if entry already exists
        e = util.get_entry(t)
        if  e is None:
            # add the title and get the content of the entry
            c = f"# {t}\n\n{request.POST['entry']}"
            # save the entry
            util.save_entry(t, c)
            # after submit go to the entry page
            return HttpResponseRedirect(reverse('entry', args=[t]))
        else:
            # if entry already exits just add a warning for the user
            msg = f"entry {t} already exists"
            msgtype = "danger"
    # if get request no message
    else:
        msg = ""
        msgtype = ""
    # render the page with form for the new page
    return render(request, "encyclopedia/new.html", {
        "msg": msg,
        "msgtype": msgtype
    })

def edit(request, entry):
    # check if entry exists
    e = util.get_entry(entry)
    if  e is None:
        # 404 if entry in the url does not exist
        return render(request, "encyclopedia/404.html", {
        })
    else:
        # if post request handle the edit form
        if request.method == "POST":
            t = entry
            # add the title and get the content of the entry
            c = f"# {t}\n\n{request.POST['entry']}"
            # save the entry
            util.save_entry(t, c)
            # after submit go to the entry page
            return HttpResponseRedirect(reverse('entry', args=[entry]))
        # if get request render the edit page
        else:
            return render(request, f"encyclopedia/edit.html", {
                "entry": entry,
                "content": e.split("\n",2)[2]
            })

def entry(request, entry):
    # check if entry exists
    e = util.get_entry(entry)
    if  e is None:
        # 404 if entry in the url does not exist
        return render(request, "encyclopedia/404.html", {
        })
    else:
        # render the entry page with a md conversion
        return render(request, f"encyclopedia/entry.html", {
            "entry": entry,
            # convert the content of the md file and remove title line and separator line
            "content": markdowner.convert(e.split("\n",2)[2])
        })

def search(request):
    if request.method == "POST":
        # get the search query
        q = request.POST['q']
        # test if the search query return a specific entry
        match = util.get_entry(q)
        # if search request does not match an entry look for matches in the list of entries
        if  match is None:
            # find entries that match the search request
            matching = [s for s in util.list_entries() if q.lower() in s.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": matching,
                # send a number of results
                "nbresults": len(matching)
            })
        # if search request matches an entry, return the entry page
        else:
            return HttpResponseRedirect(reverse('entry', args=[q]))
    # if get request return the homepage
    else:
        return HttpResponseRedirect("/")

def randomentry(request):
    # get random element in the entry list based on list_entries result
    entry = random.choice(util.list_entries())
    # return the entry page
    return HttpResponseRedirect(f"/wiki/{entry}")