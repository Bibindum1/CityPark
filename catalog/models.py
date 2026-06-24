
from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or f"category-{uuid.uuid4().hex[:8]}"

            slug = base
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = f"{self.slug}-{uuid.uuid4().hex[:4]}"
            super().save(*args, **kwargs)


class Dish(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="dishes"
    )

    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="dishes/", blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.PositiveIntegerField(default=100)
    calories = models.PositiveIntegerField(default=0)
    prep_time = models.PositiveIntegerField(default=5)
    cooking_time = models.PositiveIntegerField(default=15)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or f"dish-{uuid.uuid4().hex[:8]}"
            slug = base
            counter = 1

            while Dish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
