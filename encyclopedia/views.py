from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util
serach = ""
class NewTaskForm(forms.Form):
	serach = forms.CharField( label = "Search")


def page(request, name):
	if request.method == "GET":
		# name = request.get("name")
		entries = util.list_entries()

		if name not in entries:
			return render(request, "encyclopedia/error.html", {
			"error_msg": "The page you are looking for does not exist.",
			"form": NewTaskForm(),
		})
	# else:

		return render(request,"encyclopedia/page.html",{
		"content": markdown2.markdown(util.get_entry(name)),
		"name": name,
		"form": NewTaskForm(),
			
		})


def index(request):
	entries = util.list_entries()
	if request.method == "POST":
		search = NewTaskForm(request.POST)

		if search.is_valid():
			search = search.cleaned_data["serach"]

			if search in entries:
	 			return HttpResponseRedirect(reverse("encyclopedia:page", args=[search]))
			
			partial_match = []

			for entry in entries:

	 			if search.lower() in entry.lower():
	 				partial_match.append(entry)


			if not partial_match:
	 			return render(request, "encyclopedia/error.html",{
					"form": NewTaskForm(),
					"error_msg": "There is not matching entry"
	 			})

			
			return render(request, "encyclopedia/search.html",{
					"form": NewTaskForm(),
					"matches": partial_match
	 			})


	else:
   	 	return render(request, "encyclopedia/index.html",{
    	    "entries": entries,
      	  	"form": NewTaskForm()
   		})

def newpage(request):
	if request.method == "POST":
		data = request.POST.dict()

	
		title = data.get("title")
		
		inital_entries = util.list_entries()

		if title in inital_entries:
			return render(request, "encyclopedia/error.html", {
				"error_msg": "The page already exists",
				"form": NewTaskForm()
				})

		content = data.get("content")
		util.save_entry(title, content)
		entries = util.list_entries()
	
		return HttpResponseRedirect(reverse("encyclopedia:page", args=[title]))

	else:
		return render(request, "encyclopedia/newpage.html", {
			"form": NewTaskForm()
		})

def editpage(request, name):
	entries = util.list_entries()
	if request.method == "POST":
		data = request.POST.dict()
		title = data.get("title")
		content = data.get("content")
		util.save_entry(name, content) 
		# HttpResponseRedirect(reverse("encyclopedia:page", args=[title]))
		return render(request,"encyclopedia/page.html",{
			"content": markdown2.markdown(util.get_entry(name)),
			"name": name,
			"form": NewTaskForm(),
			})
			
	else:
		return render(request,"encyclopedia/editpage.html",{
		"content": util.get_entry(name),
		"name": name,
		"form": NewTaskForm(),
	
	})



def rand(request):
	if request.method == "GET":

		entries = util.list_entries()
		name = random.choice(entries)
		page(request, name)
		
		return render(request,"encyclopedia/randpage.html",{
		"content": markdown2.markdown(util.get_entry(name)),
		"name": name,
		"form": NewTaskForm(),
	
 	})

