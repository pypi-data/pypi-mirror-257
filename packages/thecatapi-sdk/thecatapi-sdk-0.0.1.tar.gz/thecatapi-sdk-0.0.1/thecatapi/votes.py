import json

from .base import Base


class Votes(Base):

    def get_votes(self, **kwargs):
        """
        fetch all votes
            limit: [optional] default:1 - number of results to return, up to 25 with a valid API-Key
            page: [optional] default:0 - paginate through results
            order: [optional] default:RANDOM - RANDOM | ASC | DESC
            attach_image: [optional] default:true - Add the Image matching the image_id to the response
            sub_id: [optional] Filter favourites to those with matching
        :return:
        """
        limit = kwargs.get('limit', '')
        page = kwargs.get('page', '')
        order = kwargs.get('order', '')
        attach_image = kwargs.get('attach_image', '')
        sub_id = kwargs.get('sub_id', '')
        query_string = f"limit={limit}&page={page}&order={order}&attach_image={attach_image}&sub_id={sub_id}"

        path = self._url(f'/votes?{query_string}')
        return self.make_request(path=path)

    def get_vote(self, vote_id):
        """
        get detail of a vote
        :param vote_id:
        :return:
        """
        path = self._url(f'/votes/{vote_id}')
        return self.make_request(path=path)

    def upvote(self, **kwargs):
        """
        upvote an image
        :param
            image_id
            sub_id
        :return:
        """
        data = {
            "image_id": kwargs.get('image_id', ''),
            "sub_id": kwargs.get('sub_id', ''),
            "value": 1
        }
        path = self._url(f'/votes')
        return self.make_request('POST', path, data=json.dumps(data))

    def downvote(self, **kwargs):
        """
        downvote an image
        :param
            image_id
            sub_id
        :return:
        """
        data = {
            "image_id": kwargs.get('image_id', ''),
            "sub_id": kwargs.get('sub_id', ''),
            "value": -1
        }
        path = self._url(f'/votes')
        return self.make_request('POST', path, data=json.dumps(data))

