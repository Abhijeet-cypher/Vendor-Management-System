from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from django.db.models import ExpressionWrapper, F
# from django.db.models import JSONField

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        total_orders = self.purchaseorder_set.count()

        # Calculate on-time delivery rate
        on_time_orders = self.purchaseorder_set.filter(delivery_date__lte=timezone.now()).count()
        self.on_time_delivery_rate = (on_time_orders / total_orders) * 100 if total_orders > 0 else 0

        # Calculate average quality rating
        self.quality_rating_avg = round(self.purchaseorder_set.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0, 1)

        # Calculate average response time in seconds
        response_time_expr = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=models.DurationField()
        )
        avg_response_time_delta = self.purchaseorder_set.aggregate(avg_response=Avg(response_time_expr))['avg_response'] or timedelta(seconds=0)
        avg_response_time_seconds = avg_response_time_delta.total_seconds()

        # Ensure average response time is non-negative
        self.average_response_time = max(avg_response_time_seconds, 0)

        # Calculate fulfillment rate
        fulfilled_orders = self.purchaseorder_set.filter(status='completed').count()
        self.fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0

        self.save()

    def update_response_time(self, response_time_seconds):
        total_orders = self.purchaseorder_set.count()
        total_response_time = self.purchaseorder_set.aggregate(total_response_time=Avg(models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'), output_field=models.DurationField())))['total_response_time'] or timedelta(seconds=0)
        new_total_response_time_seconds = total_response_time.total_seconds() + response_time_seconds
        self.average_response_time = new_total_response_time_seconds / total_orders if total_orders > 0 else 0
        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"



