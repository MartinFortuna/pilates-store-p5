import os
import hashlib
from django.shortcuts import redirect, render
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_marketing as MailchimpMarketing
from django.contrib import messages

# Create your views here.

api_key = os.getenv('MAILCHIMP_SECRET_KEY')
list_id = os.getenv('MAILCHIMP_AUDIENCE')


def subscribe_newsLetter(request):
    if request.method == "POST":
        email = request.POST['email']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']

        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": api_key,
        })

        userInfo = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": firstName,
                "LNAME": lastName
            }
        }

        try:
            mailchimpClient.lists.add_list_member(list_id, userInfo)
            messages.success(request, f"Thank you for subscribing!")
        except ApiClientError as error:
            if error.status_code == 400 and 'already a list mem' in error.text:
                messages.info(request, f"Already subscribed!")
            else:
                messages.error(request, f"Oops, {error.text}")
    return render(request, "home/index.html")


def unsubscribe_newsletter(request):
    if request.method == "POST":

        email = request.POST['email']
        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": api_key,
        })

        member_update = {
                    'status': 'unsubscribed',
                }

        try:
            hash = hashlib.md5(email.encode('utf-8').lower()).hexdigest()
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": "YOUR_API_KEY",
                "server": "YOUR_SERVER_PREFIX"
            })

            mailchimpClient.lists.update_list_member(
                list_id, hash, member_update,
                )
            messages.success(request, f"You are unsubscribed!")
        except ApiClientError as error:
            messages.error(request, f"Oops, {error.text}")
    return render(request, "marketing/unsubscribe_newsletter.html")
