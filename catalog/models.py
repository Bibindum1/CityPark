from django.db import models
from django.utils.text import slugify


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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название"
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Категория"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    ingredients = models.TextField(
        blank=True,
        null=True,
        verbose_name="Состав"
    )

    image = models.ImageField(
        upload_to="dishes/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )

    weight = models.PositiveIntegerField(
        default=100,
        verbose_name="Вес (г)"
    )

    calories = models.PositiveIntegerField(
        default=0,
        verbose_name="Калорийность"
    )

    prep_time = models.PositiveIntegerField(
        default=5,
        verbose_name="Подготовка (мин)"
    )

    cooking_time = models.PositiveIntegerField(
        default=15,
        verbose_name="Приготовление (мин)"
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступно"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            generated = slugify(self.name)

            if not generated:
                raise ValueError("Slug не может быть пустым. Проверь name.")



            self.slug = generated

        super().save(*args, **kwargs)

    @property
    def total_time(self):
        return self.prep_time + self.cooking_time

    def __str__(self):
        return self.name


class Order(models.Model):

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