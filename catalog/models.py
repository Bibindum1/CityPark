from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )

    slug = models.SlugField(unique=True, blank=True, null=True)

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            generated = slugify(self.name)

            if not generated:
                generated = f"dish-{uuid.uuid4().hex[:8]}"

            base = generated
            slug = base
            counter = 1

            while Dish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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
            base = slugify(self.name)

            # если slug пустой
            if not base:
                base = f"dish-{uuid.uuid4().hex[:8]}"

            slug = base
            counter = 1

            # защита от дублей
            while Dish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def total_time(self):
        return self.prep_time + self.cooking_time

    def __str__(self):
        return self.name


class Order(models.Model):
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        self.total = sum(
            item.price * item.quantity
            for item in self.items.all()
        )
        self.save()

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("accepted", "Принят"),
        ("cooking", "Готовится"),
        ("delivery", "Доставляется"),
        ("completed", "Выполнен"),
        ("cancelled", "Отменен"),
    ]

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Пользователь"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Сумма"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус"
    )

    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(
        max_length=255
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name