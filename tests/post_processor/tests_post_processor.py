from unittest.mock import patch
from django.utils.module_loading import import_string
from .models import VersatileImagePostProcessorTestModel
from ..tests import VersatileImageFieldBaseTestCase


md5_16_processor = import_string('versatileimagefield.processors.md5_16')


@patch("versatileimagefield.utils.VERSATILEIMAGEFIELD_POST_PROCESSOR", wraps=md5_16_processor)
class VersatileImageFieldPostProcessorTestCase(VersatileImageFieldBaseTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.instance = VersatileImagePostProcessorTestModel.objects.create(
            image='python-logo.jpg'
        )

    def test_post_processor(self, mocked_post_processor_function):
        """
        Ensure versatileimagefield.registry.autodiscover raises the
        appropriate exception when trying to import on versatileimage.py
        modules.
        """
        self.instance.create_on_demand = True
        self.assertEqual(
            self.instance.image.crop['100x100'].url,
            '/media/__sized__/python-logo-2c88a725748e22ee.jpg'
        )

    def test_obscured_file_delete(self, mocked_post_processor_function):
        self.assertImageDeleted(self.instance.image)
