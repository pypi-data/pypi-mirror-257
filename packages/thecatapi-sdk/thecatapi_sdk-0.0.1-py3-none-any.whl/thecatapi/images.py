import json

from .base import Base


class Images(Base):

    def get_images(self, **kwargs):
        """
        searches for all approved images depending on filters
        :param
            limit: [optional] default:1 - number of results to return, up to 25 with a valid API-Key
            page: [optional] default:0 - paginate through results
            order: [optional] default:RANDOM - RANDOM | ASC | DESC
            has_breeds: [optional] default:true - only return images with breed data
            include_breeds: [optional] default:true - Adds the 'breed' object ot the image, only if an api
            include_categories: [optional] default:true - Adds the 'breed' object ot the image, only if an api
            mime_types: [optional] default:jpg - jpg | png | gif - a comma separated strig of types to return
                    e.g. jpg,png for static, or gif for gifs
            size: [optional] default:med - thumb , small, med or full - small is perfect for Discord
            format: [optional] default:json - pass 'src' to redirect the request to the image's url
        :return
            JSON response containing list of images
        """
        limit = kwargs.get('limit')
        page = kwargs.get('page')
        order = kwargs.get('order')
        has_breeds = kwargs.get('has_breeds')
        include_breeds = kwargs.get('include_breeds')
        include_categories = kwargs.get('include_categories')
        mime_types = kwargs.get('mime_types')
        size = kwargs.get('size')
        format = kwargs.get('format')
        query_string = (f'limit={limit}&page={page}&order={order}&has_breeds={has_breeds}&include_breeds={include_breeds}'
                        f'&include_categories={include_categories}&mime_types={mime_types}&size={size}&format={format}')

        path = self._url(f'/images/search?{query_string}')
        return self.make_request(path=path)

    def get_image(self, image_id):
        """
        Returns an image matching the id passed
        :param
            image_id:
        :return
            JSON response containing image detail
        """
        path = self._url(f'/images/{image_id}')
        return self.make_request(path=path)

    def get_image_analysis(self, image_id):
        """
        Get the raw analysis results for any uploaded image
        :param
            image_id
        """
        path = self._url(f'/images/{image_id}/analysis')
        return self.make_request(path=path)

    def get_my_images(self, **kwargs):
        """
        returns images from your account, uploaded via 'api/v1/images/upload'
        :param
            limit: [optional] default:1 - number of results to return, up to 25 with a valid API-Key
            page: [optional] default:0 - paginate through results
            order: [optional] default:RANDOM - RANDOM | ASC | DESC
            sub_id: [optional]
            breed_ids: [optional]  - ids of breeds to filter by e.g beng,abys
            category_ids: [optional] ids of categories to filter by
            format: [optional] default:json - pass 'src' to redirect the request to the image's url
        :return
            JSON response containing list of images from your acct
        """
        limit = kwargs.get('limit')
        page = kwargs.get('page')
        order = kwargs.get('order')
        sub_id = kwargs.get('sub_id')
        breed_ids = kwargs.get('breed_ids')
        category_ids = kwargs.get('category_ids')
        format = kwargs.get('format')
        original_filename = kwargs.get('original_filename')
        user_id = kwargs.get('user_id')
        query_string = (
            f'limit={limit}&page={page}&order={order}&sub_id={sub_id}&breed_ids={breed_ids}&category_ids={category_ids}'
            f'&format={format}&original_filename={original_filename}&user_id={user_id}')
        path = self._url(f'/images?{query_string}')
        return self.make_request(path=path)

    # TODO: Fix upload issue
    def upload_image(self, file, sub_id=None, breed_ids=None):
        """
        Upload an image to your account
        :param
            file: - file
            sub_id: [optional] - a string you can use to segment your images, usually user id
            breed_ids: [optional] - comma separated string of breed ids contained in the image
        :return:
        """
        path = self._url(f'/images/upload')
        files = {'file': ('screenshot.png', open(file, 'rb')), 'sub_id': '1', 'breed_ids': 'abys'}
        data = {'sub_id': sub_id, 'breed_ids': breed_ids}
        return self.make_request('POST', path=path, data=data, files=files)

    def delete_image(self, image_id):
        """
        Deletes image resource
        :param
            image_id:
        """
        path = self._url(f'/images/{image_id}')
        return self.make_request('DELETE', path=path)

    def get_image_breeds(self, image_id):
        """
        Get breeds for an image
        :param
            image_id:
        """
        path = self._url(f'/images/{image_id}/breeds')
        return self.make_request(path=path)

    def update_image_breeds(self, image_id, breed_id):
        """
        Update image breed
        :param
            image_id:
            breed_id:
        """
        data = {
            "breed_id": breed_id
        }
        path = self._url(f'/images/{image_id}/breeds')
        return self.make_request('POST', path=path, data=data)

    def delete_image_breeds(self, image_id, breed_id):
        """
        delete breed
        :param
            image_id:
            breed_id:
        """
        path = self._url(f'/images/{image_id}/breeds/{breed_id}')
        return self.make_request('DELETE', path=path)
