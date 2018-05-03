from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ausgabe(models.Model):
    datum = models.DateField('Datum')
    wert = models.DecimalField("Summe",max_digits=100,decimal_places=2)
    mitbewohni = models.ForeignKey(User, related_name="von_mitbewohni", on_delete=models.CASCADE, limit_choices_to={'is_superuser':False},)
    an = models.ManyToManyField(User, related_name="an_mitbewohnis", limit_choices_to={'is_superuser':False},)
    notiz = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "Ausgabe (" + str(self.wert) + " €)"

    def __str__(self):
        return "Ausgabe (" + str(self.wert) + " €)"