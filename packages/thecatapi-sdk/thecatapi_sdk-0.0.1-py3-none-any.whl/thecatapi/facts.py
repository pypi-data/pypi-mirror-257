from .base import Base


"""
Returns an evergrowing list of Facts about Cats, Dogs and their different breeds. These have been checked for
accuracy and to be safe for schools [Premium feature]
"""


class Facts(Base):

    def get_facts(self, limit, page, order):
        """
        Get one or more Random facts and the Species. For more at a time just update the 'limit' field
        :param
            limit: [optional] default:1 - number of results to return
            page: [optional] default:0 - paginate through results
            order: [optional] default:RAND - RAND | ASC | DESC
        :return:
        """
        query_string = f"limit={limit}&page={page}&order={order}"
        path = self._url(f'/facts?{query_string}')
        return self.make_request(path=path)

    def get_random_breed_facts(self, limit, page, breed_id):
        """
        List facts about a breed
        :param
            limit: [optional] default:1 - number of results to return
            page: [optional] default:0 - paginate through results
            breed_id:
        :return:
        """
        query_string = f"limit={limit}&page={page}"
        path = self._url(f'/breeds/{breed_id}/facts?{query_string}')
        return self.make_request(path=path)

    def get_ordered_breed_facts(self, limit, page, order, breed_id):
        """
        get ordered facts about breed
        :param
            limit: [optional] default:1 - number of results to return
            page: [optional] default:0 - paginate through results
            order: [optional] default:RAND - RAND | ASC | DESC
            breed_id
        :return:
        """
        query_string = f"limit={limit}&page={page}&order={order}"
        path = self._url(f'/breeds/{breed_id}/facts?{query_string}')
        return self.make_request(path=path)
