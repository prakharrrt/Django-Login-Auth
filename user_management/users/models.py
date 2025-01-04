from django.db import models
from django.contrib.auth.models import User


# Extending the Users model to a one to one User-Profile model

class Profile(models.Model):
    # user attribute is a foreing key, est link bw user and profile models
    # The first argument of OneToOneField specifies which model the current model will be related to, 
    # which in our case is the User model. The second argument on_delete=models.CASCADE 
    # means that if a user is deleted, delete his/her profile as well.
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    avatar=models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    
    # The dunder __str__ method converts an object into its string representation which makes it 
    # more descriptive and readable when an instance of the profile is printed out. So, whenever
    #  we print out the profile of a user, it will display his/her username.
    def __str__(self):
        return self.user.username
    
    
