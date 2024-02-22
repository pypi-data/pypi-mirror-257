import pytest
from thecatapi import TheCatAPI
from thecatapi.base import Base
from thecatapi.images import Images

instance = TheCatAPI(api_key='live_FkOnFCtfJUcl5A1CvNBnaqXbX2MpjQcG2UbwI7FXr3Jkh7LfLv7EHOGQJMaGDwdU')


class TestImages(object):

    def test_get_images(self):
        response = instance.images.get_images()
        assert type(response) is list

    def test_get_image(self):
        response = instance.images.get_image(image_id='2bbSbBC-v')
        assert type(response) is dict

    def test_get_image_analysis(self):
        response = instance.images.get_image_analysis(image_id='2bbSbBC-v')
        assert type(response) is list

    def test_get_my_images(self):
        response = instance.images.get_my_images()
        assert type(response) is list

    # def test_upload_image(self):
    #     file = '/Users/ozorku/Desktop/screenshot.png'
    #     response = instance.images.upload_image(file=file)
    #     assert 'url' in response

    def test_image_breeds(self):
        response = instance.images.get_image_breeds(image_id='2bbSbBC-v')
        assert type(response) is list


