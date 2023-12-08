from django.db import models

class SkredvarslingsSted(models.Model):
    stedid = models.IntegerField(primary_key=True)
    stedsnavn = models.CharField(max_length=200)
    stedsbeskrivelse = models.CharField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.stedsnavn