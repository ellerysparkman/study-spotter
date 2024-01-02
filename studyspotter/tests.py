from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User



class HelloWorldViewTestCase(TestCase):
    def test_hello_world_view_status_code(self):
        url = reverse('hello_world')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_hello_world_view_response_content(self):
        url = reverse('hello_world') 
        response = self.client.get(url)
        self.assertContains(response, "Hello, Person-Trying-To-Log-In!")
        

class MapViewTestCase(TestCase):
    def setUser(self):
        self.user = User.objects.create_user(username='regular_user', password='Alderman2024')
        self.admin_user = User.objects.create_user(username='admin_user', password='Alderman2024', is_staff=True)

    def test_reg_map_page_status_code(self):
        self.client.login(username='regular_user', password='password')
        response = self.client.get(reverse('study-spotter:map'), follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_admin_map_page_status_code(self):
    #     # Log in as an admin user
    #     self.client.login(username='admin_user', password='password')
    #     response = self.client.get(reverse('study-spotter:map'), follow=True)
    #     self.assertEqual(response.status_code, 200)

    def test_map_page_response_content(self):
        response = self.client.get(reverse('study-spotter:map'))
        self.assertContains(response, "UVA Grounds Study Spots")
        #self.assertContains(response, "UVA Grounds Map")


# class SaveStudySpotViewTestCase(TestCase):
#     def test_save_study_spot_view(self):
#         url = reverse('study-spotter:save_studyspot')
#         data = {
#             'latitude': 10.12345,
#             'longitude': 20.54321,
#             'name': 'Test Spot',
#             'description': 'This is a test spot',
#             'author': 'Test Author'
#         }
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['message'], 'Marker saved successfully')
