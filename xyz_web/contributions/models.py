from django.db import models
from django.forms import ModelForm
from django.core.mail import send_mail

from urllib.parse import urlparse
from simple_history.models import HistoricalRecords

import secrets
import html

TOKEN_LENGTH = 10  # NB, bytes not chars.

def get_random_token():
    return secrets.token_urlsafe(TOKEN_LENGTH)


def get_video_id_youtube(video_url):
    parsed = urlparse(video_url)
    queries = parsed.query.split("&")
    for query in queries:
        key, value = query.split("=")
        if key == "v":
            return value
    return None

def get_video_id_vimeo(video_url):
    parsed = urlparse(video_url)
    id = parsed.path.strip('/')
    return id

def youtubePlayer(video_id):
    return f'<iframe width="640" height="360" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

def vimeoPlayer(video_id):
    return f'<iframe src="https://player.vimeo.com/video/{video_id}?embedparameter=value" width="640" height="360" frameborder="0" allowfullscreen></iframe>'


def player(url_parser, specific_player):
    def video_player(video_url):
        video_id = url_parser(video_url)
        video_id = html.escape(video_id)
        return specific_player(video_id)
    return video_player

parsers = {
    "youtube": get_video_id_youtube,
    "vimeo": get_video_id_vimeo,
}


players = {
    "youtube": player(get_video_id_youtube, youtubePlayer),
    "vimeo": player(get_video_id_vimeo, vimeoPlayer),
}

class Contribution(models.Model):
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
        default=get_random_token,
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
