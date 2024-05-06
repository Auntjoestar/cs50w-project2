from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Offers(models.Model):
    offerer = models.ForeignKey(
        User,
        related_name="offered_by",
        verbose_name="Offered By",
        on_delete=models.CASCADE,
    )
    offer_amount = models.PositiveIntegerField(
        blank=False, verbose_name="Offer", default=1, validators=[MinValueValidator(1)]
    )
    offered_at = models.DateTimeField(
        default=datetime.now, verbose_name="Offer created at"
    )

    def __str__(self):
        return f"Offer of {self.offer_amount} by {self.offerer.username}"


class Listing(models.Model):
    lister = models.ForeignKey(
        User, related_name="lister", on_delete=models.CASCADE, verbose_name="Listed By"
    )
    title = models.CharField(max_length=50, blank=False, verbose_name="Title")
    description = models.CharField(
        max_length=1000, blank=False, verbose_name="Description"
    )
    price = models.ForeignKey(
        Offers, verbose_name="Price", related_name="price", on_delete=models.CASCADE
    )
    imageLink = models.URLField(max_length=200, blank=True, verbose_name="Image")
    CATEGORY_CHOICES = [
        ("AR", "Armor"),
        ("PT", "Potions"),
        ("RN", "Rings"),
        ("RD", "Rods"),
        ("SL", "Scrolls"),
        ("SF", "Staffs"),
        ("WN", "Wands"),
        ("WP", "Weapons"),
        ("WI", "Wondrous Items"),
        ("OT", "Other"),
    ]
    categories = models.CharField(
        blank=True,
        choices=CATEGORY_CHOICES,
        max_length=2,
        default=CATEGORY_CHOICES[9][1],
        verbose_name="Category",
    )
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=datetime.now, verbose_name="Updated at")
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="listingWatchlist"
    )

    def __str__(self):
        return f"Listing by {self.lister.username}: {self.title}"


class Comments(models.Model):
    user = models.ForeignKey(
        User,
        related_name="commented_by",
        verbose_name="Commented By",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Listing,
        related_name="commented_on",
        verbose_name="Commented On",
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=500, blank=False, verbose_name="Comment")
    commented_at = models.DateField(
        default=datetime.now(), verbose_name="Comment created at"
    )

    def __str__(self):
        return (
            f'Comment by {self.user.username} on "{self.product.title}": {self.comment}'
        )


class Winners(models.Model):
    item = models.ForeignKey(
        Listing,
        verbose_name="Product Winned",
        related_name="product_winned",
        on_delete=models.CASCADE,
    )
    winned_by = models.ForeignKey(
        User,
        verbose_name="Winned by",
        related_name="winned_by",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateField(default=datetime.now, verbose_name="Product winned at")

    def __str__(self):
        return f"{self.item.title} winned by {self.winned_by.username}"
