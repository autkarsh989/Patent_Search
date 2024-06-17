from django.shortcuts import render, reverse
import requests
import google.generativeai as genai
from django.http import HttpResponseRedirect, JsonResponse
from .newsc import scrape_patent_data
import os
import http.client
import json
genai.configure(api_key="AIzaSyCjr-30vvDZoejP_MDDvhYbWCdLw_2XPME")



def search_patents(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        


        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()




        check_text= "give me only minimum 5-7 word to so that i can search and compare to match my idea with any other idea which is relevant, remember your response should be those 5-7 word nothing else"



        res = chat.send_message(text+check_text)
        scrape_patent_data(res.text)
        prompt="commpare both idea and tell if any thing is common in them i am giving you abstract idea of both the project with intention of identifying if my idea is different and can be put to publish and patent tell your opinion if they are similar and what way before this prompt the idea which is ours is given and after this text all the idea which are patented is there  "
        with open("data.txt","r+",encoding="utf-8") as file:
            data = file.read()
        response = chat.send_message(text+prompt+data)
        return render(request, 'search_results.html', {'results': response.text})
    elif request.method == 'GET':
        return render(request, 'search_form.html')





    #     response = requests.get(f'https://api.gemini.com/v1/search?q={query}&type=patent')
    #     if response.status_code == 200:
    #         return render(request, 'search/search_results.html', {'results': response.json()['results'][0]['title']})
    #     else:
    #         return render(request, 'search/search_results.html', {'error': 'Failed to retrieve results'})
    # return render(request, 'search/search_form.html')