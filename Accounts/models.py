from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

 




class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()





class Account(models.Model):
    User = models.ForeignKey(User, related_name='account',on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null = True)
    first_name = models.CharField(max_length=255, null = True)
    last_name = models.CharField(max_length=255, null = True)
    email = models.CharField(max_length=255, null = True)
    company_name = models.CharField(max_length=255, null = True)
    phone_number = models.CharField(max_length=255, null = True)
    documents = models.FileField(upload_to='documents', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    

class Shop(models.Model):
    subdomain = models.CharField(max_length=255, unique=True) 
    Account_id = models.IntegerField(null=True)
    shop_name = models.CharField(max_length=255, unique=True) 
    shop_description = models.TextField()
    shop_banner = models.ImageField(upload_to='banner',
                              blank=True)
    shop_logo = models.ImageField(upload_to='logo',
                              blank=True)
    shop_balance = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20, null = True)
    created = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    
    

    def __str__(self):
        return '%s' % (self.shop_name)

    
    def _get_unique_slug(self):
        slug = slugify(self.shop_name)
        unique_slug = slug
        num = 1
        while Shop.objects.filter(subdomain=unique_slug).exists():
            unique_slug = '{}-{}.{}'.format(slug, num, settings.DEFAULT_SITE_DOMAIN)
            num += 1
            print('subdomian slug',unique_slug)
        unique_slug = '{}.{}'.format(slug,settings.DEFAULT_SITE_DOMAIN)
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.subdomain:
            self.subdomain = self._get_unique_slug()
        super().save(*args, **kwargs)





class Category(models.Model):
    shop_name = models.ForeignKey(Shop, related_name='account',on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storefront:product_list_by_category',
                       args=[self.slug])

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,unique=True)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storefront:product_detail',
                       args=[self.id, self.slug])

 
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

class Order(models.Model):
    shop_name = models.ForeignKey(Shop, related_name='order',on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null = True)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)



    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    is_refunded = models.BooleanField(default=False)


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


CHOICES = (
    ('Stop by the store', 'Stop by the store'),
    ('deliver to my address', 'deliver to my address')
)

class DeliveryMethod(models.Model):
    Order = models.ForeignKey(Order,related_name='delivery',on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=40, choices=CHOICES)
                              


TRANSACTION_TYPES = (
    ('withdraw_from_shop', 'Withdraw from shop balance'),
    ('request_transfer', 'Request transfer from user'),
    ('MPESA', 'Paid by Mpesa'),
    ('refund_order', 'Refund order'),
    ('Eazzypay', 'Paid by eazzypay'),
    ('Pay_on_delivery', 'Pay on delivery')
)

class ShopTransactionActivity(models.Model):
    """
        Save accounting transactions
    """
    shop_name = models.ForeignKey(Shop, related_name='shop',on_delete=models.CASCADE)
    transaction_amount = models.FloatField(default=0.0)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    order = models.ForeignKey(Order, related_name='shop_order', null=True,on_delete=models.CASCADE)
    payment_response = models.TextField(null=True, blank=True)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    phone_used = models.CharField(null = True,max_length=255)
    is_rejected = models.BooleanField(default=True)
    payment_transaction_ref=models.CharField(max_length=100, null=True, blank=True, unique=True)
    order_transaction_ref=models.CharField(max_length=100, null=True, blank=True, unique=True)

class Campaign(models.Model):
    fullname = models.CharField(max_length=100, null=True, blank=True, unique=False)
    email_address = models.CharField(max_length=100, null=True, blank=True, unique=False)
    phone_number =  models.CharField(max_length=100, null=True, blank=True, unique=False)
    message = models.TextField()

