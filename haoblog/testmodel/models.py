from django.db import models


class One(models.Model):
    #count = models.IntegerField(editable=False, default=1)
    name = models.CharField(max_length=20)
    #count = {name: 1}

    def __unicode__(self):
        return self.name
        #return '%s %d' % (self.name, self.count[self.name])
    '''
    def __init__(self, name):
        super.__init__(self, name)'''
    '''
    def save(self, *args, **kwargs):
        try:
            if One.objects.get(name=self.name):
                One.count[self.name] += 1
                assert One.count[self.name] > 1
        except One.DoesNotExist:
            super(One, self).save(*args, **kwargs)
        try:
            one = One.objects.get(name=self.name)
            one.count += 1
            one.save()
            #super(One, self).save(*args, **kwargs)
            assert one.count > 1
        except One.DoesNotExist:
            super(One, self).save(*args, **kwargs)'''


class Many(models.Model):
    name = models.CharField(max_length=20, unique=True)
    ks = models.ForeignKey(One, related_name='one')

    def __unicode__(self):
        return 'Many- %s, %s' % (self.name, self.ks)

    def save(self, *args, **kwargs):
        one = One.objects.get(name=self.ks.name)
        if one:
            one.count += 1
        else:
            one.count = 1
        super(Many, self).save(*args, **kwargs)
