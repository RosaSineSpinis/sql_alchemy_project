from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, 'welcome.html', context)


class Menu(View):
    def get(self, request, *args, **kwargs):
        name_list = ['Change oil', 'Inflate tires', 'Get diagnostic test']
        context = {
            'name_list': name_list,

        }
        return render(request, 'menu.html', context)


ticket_process = 0
counter = 0
num = {
    "change_oil": 0,
    "change_oil_ticket_list": [],
    "inflate_tires": 0,
    "inflate_tires_ticket_list": [],
    "diagnostic": 0,
    "diagnostic_ticket_list": [],
}


class Inflate_tires(View):


    def get(self, request, link, *args, **kwargs):

        global counter

        if link == "change_oil":
            que = num["change_oil"]
            time = num["change_oil"]*2
            counter += 1
            num["change_oil_ticket_list"].append(counter)

        elif link == "inflate_tires":
            que = num["change_oil"] + num["inflate_tires"]
            time = num["change_oil"]*2 + num["inflate_tires"]*5
            counter += 1
            num["inflate_tires_ticket_list"].append(counter)
        elif link == "diagnostic":
            que = num["change_oil"] + num["inflate_tires"] + num["diagnostic"]
            time = num["change_oil"]*2 + num["inflate_tires"]*5 + num["diagnostic"]*30
            counter += 1
            num["diagnostic_ticket_list"].append(counter)


        context = {
            'que': que,
            'time': time,
        }

        num[link] += 1

        return render(request, 'inflate_tires.html', context)


class RedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        return super().get_redirect_url(*args, **kwargs)

        # return super().get_redirect_url(*args, **kwargs)

        # return render(request, 'processing.html', context)


class ProcessingView(View):

    def get(self, request, *args, **kwargs):

        context = {
            'num': num,
        }

        return render(request, 'processing.html', context)

    def post(self, request, *args, **kwargs):

        global ticket_process

        if num["change_oil_ticket_list"]:
            ticket_process = num["change_oil_ticket_list"].pop(0)
            num["change_oil"] -= 1
        elif num["inflate_tires_ticket_list"]:
            ticket_process = num["inflate_tires_ticket_list"].pop(0)
            num["inflate_tires"] -= 1
        elif num["diagnostic_ticket_list"]:
            ticket_process = num["diagnostic_ticket_list"].pop(0)
            num["diagnostic"] -= 1
        else:
            ticket_process = 0

        context = {

        }

        return redirect('/next/')
# class ProcessingView(View):
#
#     pass


class Next_view(View):

    def get(self, request, *args, **kwargs):

        text = ""
        if ticket_process == 0:
            text = "Waiting for the next client"
        else:
            text = "Next ticket #"+str(ticket_process)
        context = {
            "ticket": text
        }

        return render(request, 'next.html', context)
