from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='vendor546@example.com', vendor_code="10101")
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='vendor46541@example.com', vendor_code = "10102")
        self.purchase_order1 = PurchaseOrder.objects.create(vendor=self.vendor1, po_number='PO-001', order_date = "2024-10-10 10:00", delivery_date="2024-10-10 10:00", items ="{'soap': 'lux'}", quantity = "1", issue_date = "2024-10-10 10:00")
        self.purchase_order2 = PurchaseOrder.objects.create(vendor=self.vendor2, po_number='PO-002', order_date = "2024-10-10 10:00", delivery_date= "2024-10-10 10:00", items ="{'soap': 'lux'}", quantity ="1", issue_date = "2024-10-10 10:00")
        self.login()

    def login(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_url = reverse('login')
        login_response = self.client.post(login_url, login_data)
        token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_vendors(self):
        list_vendors_url = reverse('list_vendors')  
        response = self.client.get(list_vendors_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_vendor(self):
        url = reverse('retrieve_vendor', args=[self.vendor1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 1')


    def test_update_vendor(self):
        vendor = Vendor.objects.first()
        new_name = 'Updated Vendor Name'
        new_contact_details = 'updated_vendor@example.com'
        new_address = '123 Updated Street'
        new_vendor_code = '12345'
        url = reverse('update_vendor', args=[vendor.pk])
        data = {
            'name': new_name,
            'contact_details': new_contact_details,
            'address': new_address,
            'vendor_code': new_vendor_code
        }
        response = self.client.put(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=vendor.pk).name, new_name)


    def test_retrieve_purchase_order(self):
        purchase_order = PurchaseOrder.objects.first()
        url = reverse('retrieve_purchase_order', args=[purchase_order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_purchase_order(self):
        purchase_order = PurchaseOrder.objects.first()
        url = reverse('delete_purchase_order', args=[purchase_order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(PurchaseOrder.DoesNotExist):
            PurchaseOrder.objects.get(pk=purchase_order.pk)

    
    def test_retrieve_vendor_performance(self):
        vendor = Vendor.objects.first()
        url = reverse('retrieve_vendor_performance', args=[vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_acknowledge_purchase_order(self):
        purchase_order = PurchaseOrder.objects.first()
        url = reverse('acknowledge_purchase_order', args=[purchase_order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', vendor_code="12345")
        purchase_order = PurchaseOrder.objects.create(
        po_number="PO-0010",
        order_date="2024-05-01T10:00:00",
        delivery_date="2024-05-10T10:00:00",
        items='{"name": "Product A", "quantity": 2}',
        quantity=5,
        status="Pending",
        issue_date="2024-05-01T10:00:00",
        vendor=vendor
        )
        updated_data = {
            "po_number": "PO-001-updated",
            "order_date": "2024-05-01T10:00:00",
            "delivery_date": "2024-05-10T10:00:00",
            "items": 
                '{"name": "Product A", "quantity": 2}',
            "quantity": 5,
            "status": "Completed",
            "issue_date": "2024-05-01T10:00:00",
            "vendor": vendor.pk
        }

        url = reverse('update_purchase_order', args=[purchase_order.pk])
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_purchase_order = PurchaseOrder.objects.get(pk=purchase_order.pk)
        self.assertEqual(updated_purchase_order.po_number, 'PO-001-updated')
        self.assertEqual(updated_purchase_order.status, 'Completed')
