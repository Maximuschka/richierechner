from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Mitbewohni(models.Model):
#     name = models.CharField(max_length=100)
#     mail = models.EmailField(max_length=100)

#     def __str__(self): 
#         return self.name

class Ausgabe(models.Model):
    datum = models.DateField('Datum')
    wert = models.DecimalField("Summe",max_digits=100,decimal_places=2)
    mitbewohni = models.ForeignKey(User, on_delete=models.CASCADE)
    notiz = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "Ausgabe (" + str(self.wert) + " €)"

    def __str__(self):
        return "Ausgabe (" + str(self.wert) + " €)"


class Ausgleichszahlung(models.Model):
    von = models.ForeignKey(User, on_delete=models.CASCADE, 
                            blank=True, null=True, related_name='von')
    an = models.ForeignKey(User, on_delete=models.CASCADE, 
                            blank=True, null=True, related_name='an')
    datum = models.DateField('Date')
    wert = models.DecimalField("Summe",max_digits=100,decimal_places=2)

    def __unicode__(self):
        return "Ausgleichszahlung (" + str(self.wert) + " €)"



    # erste_agz = Ausgleichszahlung.objects.all().order_by("datum")
