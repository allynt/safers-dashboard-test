from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SingletonMixin(models.Model):
    """
    Mixin to turn a model into a singleton
    """
    class Meta:
        abstract = True

    DEFAULT_SINGLETON_ID = 1

    ERROR_MESSAGE = _("Only one instance of a Singleton is allowed.")

    _singleton_id = models.IntegerField(
        default=DEFAULT_SINGLETON_ID,
        editable=False,
        help_text=_(
            "An ID to use for this mixin, "
            "in case the model uses some non-standard PK."
        ),
    )

    def clean(self, *args, **kwargs):
        """
        Prevent saving more than one singleton via a form.
        This is relevant for the Django Admin Forms.
        """
        if not self.pk and self.__class__.objects.count() > 0:
            raise ValidationError(self.ERROR_MESSAGE)

    def save(self, *args, **kwargs):
        if self.pk or not self.__class__.objects.count():
            return super().save(*args, **kwargs)
        else:
            # TODO: MAY WANT TO CONDITIONALLY RAISE ERROR ON SAVE
            pass

    @classmethod
    def load(cls):
        """
        Returns the one-and-only singleton instance
        """
        obj, _ = cls.objects.get_or_create(_singleton_id=cls.DEFAULT_SINGLETON_ID)
        return obj
