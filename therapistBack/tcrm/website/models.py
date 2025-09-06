from django.db import models
from django.utils import timezone


class Lead(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    
    # Status choices for better data integrity
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        ordering = ['-created_at']


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        ordering = ['full_name']


class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField()
    
    # Session type choices
    SESSION_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('family', 'Family'),
        ('couple', 'Couple'),
        ('assessment', 'Assessment'),
    ]
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES)
    notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.session_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-session_date']


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Invoice status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.full_name}"

    # class Meta:
    #     ordering = ['-created_at']


class InvoiceSession(models.Model):
    """Junction table linking invoices to sessions (many-to-many relationship)"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_sessions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='invoice_sessions')

    def __str__(self):
        return f"Invoice {self.invoice.invoice_number} - Session {self.session.id}"

    class Meta:
        unique_together = ['invoice', 'session']


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment method choices
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('paypal', 'PayPal'),
    ]
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    def __str__(self):
        return f"Payment ${self.amount} for Invoice {self.invoice.invoice_number}"

    class Meta:
        ordering = ['-payment_date']


class Todo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='todos')
    description = models.TextField()
    due_date = models.DateTimeField()
    
    # Todo status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Todo for {self.client.full_name}: {self.description[:50]}"

    class Meta:
        ordering = ['due_date']
        verbose_name_plural = 'Todos'


class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='client_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} - {self.client.full_name}"

    class Meta:
        ordering = ['-uploaded_at']


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    
    # Task status choices
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f"{self.title} - {self.assigned_to}"

    class Meta:
        ordering = ['due_date']


class Meeting(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='meetings')
    meeting_date = models.DateTimeField()
    
    # Meeting type choices
    MEETING_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('assessment', 'Assessment'),
        ('review', 'Review'),
        ('intake', 'Intake'),
    ]
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES)
    meeting_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.meeting_type} with {self.client.full_name} - {self.meeting_date}"

    class Meta:
        ordering = ['meeting_date']


class ProgressNote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='progress_notes')
    note_date = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return f"Progress Note for {self.client.full_name} - {self.note_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-note_date']


class RegistrationLink(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='registration_links')
    link_token = models.CharField(max_length=255, unique=True)
    sent_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Registration link for {self.lead.full_name} - {'Used' if self.used else 'Unused'}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        ordering = ['-sent_at']

class Services(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()  # Duration of the service in hours, minutes, etc.sampll durartion - e.g., 1 hour
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/services/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question']

class Testimonials(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='testimonials')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Assuming a rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.client.full_name} - Rating: {self.rating}"

    class Meta:
        ordering = ['-created_at']

class ContactFormSubmission(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-submitted_at']