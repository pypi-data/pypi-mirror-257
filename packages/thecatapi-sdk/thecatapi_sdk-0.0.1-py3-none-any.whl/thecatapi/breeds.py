from .base import Base


class Breeds(Base):
    def get_breeds(self, **kwargs):
        """
        Get all existing breeds
        :param
            limit: [optional] default:10 - number of results to return
            page: [optional] default:0 - paginate through results
        :return:
        """
        limit = kwargs.get('limit', '')
        page = kwargs.get('page', '')
        query_string = f"limit={limit}&page={page}"
        path = self._url(f'/breeds?{query_string}')
        return self.make_request(path=path)

    def get_breed(self, breed_id):
        """
        Get a breed
        :param
            breed_id:
        :return:
        """
        path = self._url(f'/breeds/{breed_id}')
        return self.make_request(path=path)

    # TODO: Endpoint not working as expected. Check why
    def get_breed_facts(self, breed_id=None):
        """
        Get facts about a breed
        :param
            breed_id:
        :return:
        """
        path = self._url(f'/breeds/{breed_id}/facts')
        return self.make_request(path=path)

    def search_breed(self, q=None, attach_image=None):
        """
        Lookup/search for breeed
        :param
            q:  search term for breed name
            attach_image: [optional] default:true - whether to attach the reference_image_id image or not
        :return:
        """
        query_string = f"q={q}&attach_image={attach_image}"
        path = self._url(f'/breeds/search?{query_string}')
        return self.make_request(path=path)
