from django.test import TestCase
from api.models import User,Order,Product
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user=User.objects.create_superuser(username='admin',password='admin123')
        self.normal_user=User.objects.create_superuser(username='user',password='user123')
        self.product=Product.objects.create(
            name='product testing',
            description='product testing description',
            price=100,
            stock=10
        )
        self.url=reverse('product-detail',kwargs={'product_id':self.product.pk})

    def test_get_product(self):
        response=self.client.get(self.url)    
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['name'],self.product.name)

    def test_unauthorized_product_update(self):
        data={'name':'update product'}
        response=self.client.put(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_update(self):
        response=self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_delete_product(self):
        self.client.login(username='admin',password='admin123')
        response=self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.filter(pk=self.product.pk).exists())
