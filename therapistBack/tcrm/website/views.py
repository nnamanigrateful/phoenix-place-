from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone


# Create your views here.
def home(request):

    if request.method == 'POST':
        # Handle form submission 
        lead_first_name = request.POST.get('firstName')
        lead_last_name = request.POST.get('lastName')
        lead_email = request.POST.get('email')
        lead_phone = request.POST.get('phone')
        lead_message = request.POST.get('message')

        #validate lead info
        if lead_first_name and lead_last_name and lead_email and lead_phone and lead_message:
            try:
                # Here you would typically save the lead to the database
                messages.success(request, 'Your message has been sent successfully!')
                subject = f"New Cotact Form Submission from {lead_first_name} {lead_last_name}"
                email_message = f""" 
    New Contact Form Submission recieved:

    Name: {lead_first_name} {lead_last_name}
    Email: {lead_email}
    Phone: {lead_phone}

    Message: {lead_message}

    Time: 
    """
                send_mail(
                    subject= subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                    
            except Exception as e:
                # Handle email sending errors
                messages.error(request, 'There was an error sending your message. Please try again.')
                print(f"Email sending error: {e}")  # For debugging
                
        else:
            # Handle missing required fields
            messages.error(request, 'Please fill in all required fields.')
        
        # Redirect to prevent form resubmission on refresh
        return HttpResponseRedirect(reverse('home'))  # Adjust the URL name as needed
    

        
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})
    
def services(request):
    return render(request, 'services.html', {})
   
def login_admin(request):
    pass
def logout_admin(request):
    pass