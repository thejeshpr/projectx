from django.db import models
import uuid

from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('crawler:category-detail', kwargs={"pk": self.pk})


class SiteConf(models.Model):
    base_url = models.CharField(max_length=250, blank=True, null=True)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, related_name='site_confs', blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    extra_data_json = models.CharField(max_length=2000, blank=True, null=True)
    icon = models.CharField(max_length=50, default='las la-question-circle', blank=True, null=True)
    is_locked = models.BooleanField(default=False)
    name = models.CharField(max_length=50, unique=True)
    ns_flag = models.BooleanField(default=False)
    scraper_name = models.CharField(max_length=25, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return f'<SiteConf: {self.name}>'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(SiteConf, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('crawler:siteconf-detail', kwargs={'pk': self.pk})


class Job(models.Model):
    JOB_STATUS = (
        ('NEW', 'NEW'),
        ('RUNNING', 'RUNNING'),
        ('SUCCESS', 'SUCCESS'),
        ('ERROR', 'ERROR'),
        ('NO-TASK', 'NO-TASK')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, null=True)
    elapsed_time = models.IntegerField(blank=True, null=True)
    site_conf = models.ForeignKey('SiteConf', on_delete=models.CASCADE, related_name='jobs')
    status = models.CharField(max_length=20, choices=JOB_STATUS, default="NEW")


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.TextField(blank=True, null=True)
    is_bookmarked = models.BooleanField(default=False)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=500)
    site_conf = models.ForeignKey('SiteConf', on_delete=models.CASCADE, related_name='tasks')
    unique_key = models.CharField(max_length=2500, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True, max_length=2500)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Task: {self.name}>'


class ExtraTaskData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='extra_data')
    data = models.CharField(max_length=2000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConfigValues(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=20, blank=True, null=True, unique=True)
    val = models.CharField(max_length=250, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f'<Task: {self.key}>'

    def save(self, *args, **kwargs):
        self.key = self.key.lower()
        super(ConfigValues, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('crawler:config-value-detail', kwargs={'pk': self.pk})
