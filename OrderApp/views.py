# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Modules Imports related to Django starts here
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect, \
    requires_csrf_token, ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotFound, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
# Modules Imports related to Django ends here

# Python System module imports starts here
from datetime import datetime
import json
import inspect
# Python System module imports ends here

# Project related module imports starts here
from OrderApi.constants import *
from .models import *
# Project related module imports ends here


class Order(View):
    def __init__(self):
        self.response = {}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Order, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # Load the order fields to order_data
        try:
            order_data = json.loads(request.body)
        except ValueError as e:
            return HttpResponseBadRequest(json.dumps(INVALID_INPUT_JSON),
                                          content_type='application/json')

        # Create a Order object
        order = Order(**order_data)

        # Validate all vields coming for a order
        try:
            order.clean_fields()
        except ValidationError as e:
            # Return 4xx for validation errors
            return HttpResponseBadRequest(json.dumps(e.message_dict),
                                          content_type='application/json')

        # Save the new order
        order.save()
        return HttpResponse(json.dumps(model_to_dict(order)),
                            content_type='application/json')

    def get(self, request, *args, **kwargs):

        # Delete all keys in the kwargs if the value is None
        kwargs = dict((k, v) for k, v in kwargs.iteritems() if v)

        # Filter Order orders based on the keys in kwargs
        order_arr = OrderLine.objects.filter(**kwargs)\
            .values('id', 'product__name', 'shipping_amount',
                    'shipping_amount', 'order__order_subtotal', 
                    'order__customer__name', 'order__customer__email', 'status')
        if len(order_arr) == 0:
            return HttpResponseNotFound(json.dumps(NO_order_ERROR),
                                        content_type='application/json')

        return HttpResponse(json.dumps(list(order_arr)),
                            content_type='application/json')

    def put(self, request, *args, **kwargs):

        # Load the order fields to order_data
        try:
            order_data = json.loads(request.body)
        except ValueError as e:
            return HttpResponseBadRequest(json.dumps(INVALID_INPUT_JSON),
                                          content_type='application/json')

        # get the Order object
        try:
            order = Order.objects.get(id=kwargs["id"])

        except (Order.DoesNotExist, KeyError, ValueError) as e:
            return HttpResponseBadRequest(json.dumps(INVALID_INPUT_JSON),
                                          content_type='application/json')

        # Set all keys with new values
        for (key, value) in order_data.items():
            setattr(order, key, value)

        # Validate all vields coming for a order
        try:
            order.clean_fields()
        except ValidationError as e:
            # Return 4xx for validation errors
            return HttpResponseBadRequest(json.dumps(e.message_dict),
                                          content_type='application/json')

        # Save the updated order
        order.save()
        return HttpResponse(json.dumps(model_to_dict(order)),
                            content_type='application/json')

    def delete(self, request, *args, **kwargs):

        # Load the order fields to order_data
        try:
            order_data = json.loads(request.body)
        except ValueError as e:
            return HttpResponseBadRequest(json.dumps(INVALID_INPUT_JSON),
                                          content_type='application/json')

        # get the Order object
        try:
            order = Order.objects.get(id=kwargs["id"])

        except (Order.DoesNotExist, KeyError, ValueError) as e:
            return HttpResponseBadRequest(json.dumps(NO_order_ERROR),
                                          content_type='application/json')

        else:
            order.status = -1
            order.save()
        return HttpResponse(json.dumps(self.response),
                            content_type='application/json')
