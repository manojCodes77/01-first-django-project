from djongo import models
from bson import ObjectId
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Increased length for hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name

    def check_password(self, raw_password):
        """
        Check if the provided raw password matches the hashed password
        """
        return django_check_password(raw_password, self.password)

    def set_password(self, raw_password):
        """
        Hash the password and save it
        """
        self.password = make_password(raw_password)

    def clean(self):
        """
        Validate the model fields
        """
        # Validate name
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Name must be at least 2 characters long'})

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValidationError({'email': 'Invalid email format'})

        # Validate password length when setting for the first time
        if not self._id and len(self.password) < 8:  # Changed from self.id to self._id
            raise ValidationError({'password': 'Password must be at least 8 characters long'})

    def save(self, *args, **kwargs):
        """
        Override save method to ensure validation is called
        """
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """
        Property to check if user is active
        Can be extended based on your needs
        """
        return True

    def to_dict(self):
        """
        Convert user object to dictionary (useful for JSON responses)
        """
        return {
            '_id': str(self._id),  # Convert ObjectId to string
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def id(self):
        """
        Provide compatibility with id attribute
        """
        return self._id