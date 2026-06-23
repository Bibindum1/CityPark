from django.db import models
from django.core.exceptions import ValidationError


class RestaurantInfo(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название ресторана"
    )

    slogan = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Слоган"
    )

    description = models.TextField(
        verbose_name="Описание"
    )

    address = models.CharField(
        max_length=255,
        verbose_name="Адрес"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    email = models.EmailField(
        verbose_name="Email"
    )

    working_hours = models.CharField(
        max_length=100,
        verbose_name="Время работы"
    )

    image = models.ImageField(
        upload_to="restaurant/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Информация о ресторане"
        verbose_name_plural = "Информация о ресторане"

    def __str__(self):
        return self.name


class Booking(models.Model):

    STATUS_CHOICES = [
        ("new", "Новое"),
        ("confirmed", "Подтверждено"),
        ("completed", "Завершено"),
        ("cancelled", "Отменено"),
    ]

    full_name = models.CharField(
        max_length=150,
        verbose_name="Имя"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )

    booking_date = models.DateField(
        verbose_name="Дата"
    )

    booking_time = models.TimeField(
        verbose_name="Время"
    )

    guests = models.PositiveIntegerField(
        default=2,
        verbose_name="Количество гостей"
    )

    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.booking_date})"


class Table(models.Model):
    number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Номер столика"
    )

    seats = models.PositiveIntegerField(
        verbose_name="Количество мест"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Доступен"
    )

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"
        ordering = ["number"]

    def __str__(self):
        return f"Столик №{self.number}"


class Review(models.Model):
    author = models.CharField(
        max_length=150,
        verbose_name="Автор"
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="Оценка"
    )

    text = models.TextField(
        verbose_name="Отзыв"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.author

class Booking(models.Model):
    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_NEW, "Новая"),
        (STATUS_CONFIRMED, "Подтверждена"),
        (STATUS_CANCELLED, "Отменена"),
    )

    full_name = models.CharField("Полное имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email", blank=True, null=True)

    booking_date = models.DateField("Дата брони")
    booking_time = models.TimeField("Время брони")

    guests = models.PositiveSmallIntegerField("Гостей", default=1)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    comment = models.TextField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("booking_date", "booking_time")
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.full_name} — {self.booking_date} {self.booking_time}"


    def clean(self):
        exists = Booking.objects.filter(
            table=self.table,
            date=self.date,
            time=self.time
        ).exclude(pk=self.pk).exists()

        if exists:
            raise ValidationError("Этот стол уже занят на это время")