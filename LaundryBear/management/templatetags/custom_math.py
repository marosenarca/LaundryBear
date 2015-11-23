from django import template
from database.models import LaundryShop, Price, Service, UserProfile, Transaction, Order, default_date
from decimal import *

register = template.Library()

@register.filter
def divide(value, arg):
	return value/arg

@register.filter
def multiply(value, arg):
	return value*arg

@register.filter
def add_all(value):
	sum = 0
	for i in value:
		sum+=(i.price.price*i.pieces)/7
	TWOPLACES = Decimal(10) ** -2 	
	sum = Decimal(sum).quantize(TWOPLACES)
	return sum