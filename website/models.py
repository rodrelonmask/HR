from django.db import models

class Record(models.Model):
    MONTH_CHOICES = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),]
    def generate_year_choices():
        return [(str(year), str(year)) for year in range(2000, 3000)]
    
    def generate_day_choices():
        return [(str(year), str(year)) for year in range(1, 32)]
    
    YEAR_CHOICES = generate_year_choices()

    DAY_CHOICES = generate_day_choices()

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    platform = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    language = models.CharField(max_length=20)
    language1 = models.CharField(max_length=20)
    language2 = models.CharField(max_length=20)
    language3 = models.CharField(max_length=20)
    language4 = models.CharField(max_length=20)
    language5 = models.CharField(max_length=20)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Select', 'Select')], default='Select')
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Select', 'Select')], default='Select')
    rate_type = models.CharField(max_length=20, choices=[('Hourly', 'Hourly'), ('Per minute', 'Per minute'), ('Select', 'Select')], default='Select')
    specificrate = models.CharField(max_length=50, null=True)
    contract_type = models.CharField(max_length=20, choices=[('Vendor', 'Vendor'), ('Freelancer', 'Freelancer'), ('Select', 'Select')], default='Select')
    agent_type = models.CharField(max_length=20, choices=[('OPI', 'OPI'), ('VRI', 'VRI'), ('On-site', 'On-site'), ('Translator', 'Translator'), ('Transcriber', 'Transcriber'), ('Select', 'Select')], default='Select')
    note = models.TextField(blank=True, null=True)
    startdateM = models.CharField(max_length=20, choices=MONTH_CHOICES, default='Month')
    startdateD = models.CharField(max_length=2, choices=DAY_CHOICES, default='Day')
    startdateY = models.CharField(max_length=4, choices=YEAR_CHOICES, default='Year')

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")