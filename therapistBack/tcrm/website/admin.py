from django.contrib import admin
from .models import Client, ContactFormSubmission, Faq, Lead, Services, Task, Document, Meeting, Payment, ProgressNote, RegistrationLink, Session, Testimonials, Todo, InvoiceSession
# Register your models here.
admin.site.register(Client)
admin.site.register(ContactFormSubmission)
admin.site.register(Faq)
admin.site.register(Lead)
admin.site.register(Services)
admin.site.register(Task)
admin.site.register(Document)
admin.site.register(Meeting)
admin.site.register(Payment)
admin.site.register(ProgressNote)
admin.site.register(RegistrationLink)
admin.site.register(Session)
admin.site.register(Testimonials)
admin.site.register(Todo)
admin.site.register(InvoiceSession)