# from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest
# from django.template.loader import render_to_string

# #from lists.views import home_page

# from .models import City

# class TestTag(TestCase):

#     def test_city_create(self):
#         new_city = City.objects.create(name='Hong Kong')
#         self.assertEqual(new_city.name, 'Hong Kong')
#         self.assertEqual(new_city.slug, 'hong-kong')

#     # def test_root_url_resolves_to_home_page_view(self):
#     #     found = resolve('/')
#     #     self.assertEqual(found.func, home_page)

#     # def test_home_page_returns_correct_html(self):
#     #     request = HttpRequest()
#     #     response = home_page(request)
#     #     html = response.content.decode('utf8')
#     #     expected_html = render_to_string('home.html')
#     #     self.assertEqual(html, expected_html)
#     #     # self.assertTrue(html.startswith('<html>'))
#     #     # self.assertIn('<title>To-Do lists</title>', html)
#     #     # self.assertTrue(html.strip().endswith('</html>'))