# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from OrderApi.utils import tele_match

class Product(models.Model):
    """This class represents the Product model."""
    name = models.TextField(null=True, Blank=True)
    desc = models.TextField(null=True, Blank=True)
    product_type = models.CharField(max_length=255)
    unit_price_amount = models.DecimalField(max_digits=19, decimal_places=2)
    unit_price_currency = models.CharField(max_length=255)
    msrp_amount = models.DecimalField(max_digits=19, decimal_places=2)
    msrp_currency = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{} {} {}".format(self.name, self.desc, self.product_type)

class Customer(models.Model):
    """This class represents the Customer model."""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, validators=[tele_match])
    email = models.EmailField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # 0: Active, 1: Inactive, -1: Deleted
    status = models.IntegerField(default=0)
    mailing_street_1 = models.CharField(max_length=255)
    mailing_street_2 = models.CharField(max_length=255)
    mailing_city = models.CharField(max_length=255)
    mailing_state = models.CharField(max_length=255)
    mailing_country = models.CharField(max_length=255)
    mailing_zipcode = models.CharField(max_length=255)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{} {} {}".format(self.title, self.first_name, self.last_name)

class ShippingAddress(models.Model):
    """This class represents the ShippingAddress model."""
    customer = models.ForeignKey(Customer, models.SET_NULL)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, validators=[tele_match])
    email = models.EmailField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # 0: Active, 1: Inactive, -1: Deleted
    status = models.IntegerField(default=0)
    shipping_street_1 = models.CharField(max_length=255)
    shipping_street_2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)
    shipping_zipcode = models.CharField(max_length=255)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{} {} {}".format(self.title, self.first_name, self.last_name)

class Order(models.Model):
    """This class represents the Order model."""
    customer = models.ForeignKey(Customer, models.SET_NULL)
    # 0: Active, 1: Inactive, -1: Deleted
    status = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    shipping_method = models.CharField(max_length=255)
    shipping_amount = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_currency = models.CharField(max_length=255)
    shipping_address = models.ForeignKey(ShippingAddress, models.SET_NULL)
    order_subtotal = models.DecimalField(max_digits=19, decimal_places=2)
    spl_instruction = models.TextField(null=True, Blank=True)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{} {} {}".format(self.customer.title, self.customer.first_name, self.customer.last_name)

class OrderLine(models.Model):
    """This class represents the OrderLine model."""
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, models.SET_NULL)
    order = models.ForeignKey(Order, models.SET_NULL)
    tax_amount = models.DecimalField(max_digits=19, decimal_places=2)
    tax_currency = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_amount = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_currency = models.CharField(max_length=255)
    desc = models.TextField(null=True, Blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    order_line_amount = models.DecimalField(max_digits=19, decimal_places=2)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{} {} {}".format(self.customer.title, self.customer.first_name, self.customer.last_name)


