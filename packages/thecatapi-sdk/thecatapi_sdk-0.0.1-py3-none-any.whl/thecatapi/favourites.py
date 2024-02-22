from .base import Base


class Favourites(Base):
    def get_favourites(self):
        """
        list favourites
        """
        path = self._url(f'/favourites')
        return self.make_request(path=path)

    def get_favourite(self, favourite_id):
        """
        Fetch detail of favourite
        :param
            favourite_id:
        :return:
        """
        path = self._url(f'/favourites/{favourite_id}')
        return self.make_request(path=path)

    def create_favourite(self, image_id, sub_id):
        """
        Add image to favourite
        :param
            image_id:
            sub_id:
        :return:
        """
        body = {
            "image_id": image_id,
            "sub_id": sub_id
        }
        path = self._url(f'/favourites')
        return self.make_request('POST', path=path, data=body)

    def delete_favourite(self, favourite_id):
        """
        Delete favourite
        :param
            favourite_id:
        :return:
        """
        path = self._url(f'/favourites/{favourite_id}')
        return self.make_request('DELETE', path=path)