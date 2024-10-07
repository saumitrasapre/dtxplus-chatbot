from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    medical_condition = models.TextField(null=True,blank=True) 
    medication_regimen = models.TextField(null=True, blank=True)  
    last_appointment_datetime = models.DateTimeField(null=True, blank=True)
    next_appointment_datetime = models.DateTimeField(null=True, blank=True)
    doctors_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(default=0)
    additional_entities = models.TextField(null=True,blank=True) 
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = timezone.now()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        else:
            self.age = 0  # If date_of_birth is not set, age can be set to 0 or null.
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
