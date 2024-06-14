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
        
        check_text= "give me only 10 keywords from the given text."



        # model = genai.GenerativeModel("gemini-pro")
        # chat = model.start_chat()
        # res = chat.send_message(text+check_text)


        conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")

        payload = {
         "messages": [
        {"role": "user", "content": text + check_text}
             ],
              "temperature": 0.9,
          "top_k": 5,
          "top_p": 0.9,
          "max_tokens": 256,
          "web_access": False
        }

        headers = {
        'x-rapidapi-key': "56fa936c7dmsh10599aba8d55b2fp18d5e4jsnbc722c84b59e",
        'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
        'Content-Type': "application/json"
        }

        conn.request("POST", "/geminipro", json.dumps(payload).encode(), headers)
        res = conn.getresponse()
        data = res.read()
        


        scrape_patent_data(data)
        prompt="commpare both idea and tell if any thing is common in them i am giving you abstrat idea of both the project with intentiono of identifying if my idea is different and can be put to publish and patent tell your opinion if they are similar and what way before this prompt the idea which is ours is given and after this text all the idea which are on google patent is there  "
        with open("data.txt","r+",encoding="utf-8") as file:
            data = file.read()


        # response = chat.send_message(text+prompt+data)
        payload2 = {
         "messages": [
        {"role": "user", "content": text+prompt+data}
             ],
              "temperature": 0.9,
          "top_k": 5,
          "top_p": 0.9,
          "max_tokens": 256,
          "web_access": False
        }
        conn.request("POST", "/geminipro", json.dumps(payload2).encode(), headers)
        res2 = conn.getresponse()
        response = res2.read()





        return render(request, 'search_results.html', {'results': response.decode('utf-8')})
    






    
    elif request.method == 'GET':
        return render(request, 'search_form.html')





    #     response = requests.get(f'https://api.gemini.com/v1/search?q={query}&type=patent')
    #     if response.status_code == 200:
    #         return render(request, 'search/search_results.html', {'results': response.json()['results'][0]['title']})
    #     else:
    #         return render(request, 'search/search_results.html', {'error': 'Failed to retrieve results'})
    # return render(request, 'search/search_form.html')