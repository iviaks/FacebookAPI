from django.db import models


class FacebookPage(models.Model):
    access_token = models.TextField()
    original_id = models.TextField()

    class Meta:
        verbose_name = "Facebook page"
        verbose_name_plural = "Facebook pages"

    def __str__(self):
        return self.original_id


class FacebookUser(models.Model):
    psid = models.TextField()

    class Meta:
        verbose_name = "Facebook user"
        verbose_name_plural = "Facebook users"

    def __str__(self):
        return self.psid


class FacebookLabel(models.Model):
    title = models.TextField(default='')
    label_id = models.TextField()

    class Meta:
        verbose_name = "Facebook label"
        verbose_name_plural = "Facebook labels"

    def __str__(self):
        return self.label_id


class FacebookUserLabel(models.Model):
    owner = models.ForeignKey(FacebookUser)
    page = models.ForeignKey(FacebookPage)
    label = models.ForeignKey(FacebookLabel)

    class Meta:
        verbose_name = "Facebook user label"
        verbose_name_plural = "Facebook user labels"

    def __str__(self):
        return self.label_id
