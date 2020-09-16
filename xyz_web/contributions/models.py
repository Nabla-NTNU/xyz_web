from django.db import models

import secrets

TOKEN_LENGTH = 10  # NB, bytes not chars.

def get_random_token():
    return secrets.token_urlsafe(TOKEN_LENGTH)


class Contribution(models.Model):
    name = models.CharField(max_length=50)
    video_link = models.URLField(help_text="Lenke til Vimeo eller YouTube video.")
    description = models.TextField()

    def __str__(self):
        return f"Contribution {self.name}"


class Vote(models.Model):
    username = models.CharField(max_length=20)
    contribution = models.ForeignKey(
        'Contribution',
        on_delete=models.CASCADE,
    )
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(
        max_length=2*TOKEN_LENGTH,
        default=get_random_token,
        unique=True
    )

    def __str__(self):
        return f"Vote by {self.username} for {self.contribution.name}"

    def send_confirm_challenge_mail(self):
        """Sends a confirmation mail to the user, with a link the user has
        to click in order to confirm the vote."""
        return

    def send_confirmed_mail(self):
        """Sends a mail to the user confirming their vote."""
