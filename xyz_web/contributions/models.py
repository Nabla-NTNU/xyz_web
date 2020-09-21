from functools import partial
from urllib.parse import urlparse

from django.core.mail import send_mail
from django.db import models
from django.forms import ModelForm
from simple_history.models import HistoricalRecords

from .utils import get_random_token, parsers, players

TOKEN_LENGTH = 10  # NB, bytes not chars.


class Contribution(models.Model):
    """A contribution consisting of a video.
    Has the ability to return a text string representing a
    html-embeded player of the video, through the method `video_player`.
    """

    name = models.CharField(max_length=50)
    contact_email = models.EmailField()
    video_link = models.URLField(help_text="Lenke til Vimeo eller YouTube video.")
    description = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return f"Contribution {self.name}"

    def number_of_votes(self):
        return self.vote_set.count()

    def get_video_service(self):
        # Assume <playername>.com. TODO: more sophisticated
        parsed = urlparse(self.video_link)
        # TODO exception handling
        netloc = parsed.netloc
        if "youtube" in netloc.lower():
            return "youtube"
        elif "vimeo" in netloc.lower():
            return "vimeo"

    def video_id(self):
        return parsers[self.get_video_service()](self.video_link)
    
    def video_player(self):
        return players[self.get_video_service()](self.video_link)


class Vote(models.Model):
    username = models.CharField(max_length=20, unique=True)
    contribution = models.ForeignKey(
        'Contribution',
        on_delete=models.CASCADE,
    )
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(
        max_length=2*TOKEN_LENGTH,
        default=partial(get_random_token, TOKEN_LENGTH),
        unique=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"Vote by {self.username} for {self.contribution.name}"

    def confirm(self):
        if self.confirmed:
            pass # TODO: throw AlreadyConfirmedException
        self.confirmed = True
        self.save()

    def save(self, *args, **kwargs):
        # If no pk, we are creating (not updating) the Vote, so send email.
        if not self.pk:
            self.send_confirm_challenge_mail()
        return super().save(*args, **kwargs)

    def send_confirm_challenge_mail(self):
        """Sends a confirmation mail to the user, with a link the user has
        to click in order to confirm the vote."""

        # TODO: better solution here. Maybe use sites framework?
        #domain = self.request.META['HTTP_HOST']
        domain = "localhost:8000"
        link = "https://" + domain + "/confirm/" + self.confirmation_token
        msg = f"Hei, \n\
\n\
        Vi trenger at du bekrefer din stemme på {self.contribution}.\n\
        Trykk på denne lenken: <a href=\"{link}\">trykk meg</a>.\n\
\n\
        Mvh. WebKom Nabla"

        send_mail(
            'Bekreft XYZ stemme',
            msg,
            'webkom@nabla.ntnu.no',
            [self.username + "@stud.ntnu.no"],
            fail_silently=False,
        )

    def send_confirmed_mail(self):
        """Sends a mail to the user confirming their vote."""
