from django.conf import settings
import redis
from rest_framework.views import APIView
from rest_framework.response import Response

# Redis
redis_instance = redis.Redis(host='redis', port=settings.REDIS_PORT, db=0)


class TestView(APIView):
    def post(self, request):
        req_data = request.data
        if req_data['symbol'] == '' and req_data['exchange'] == '':
            response_data = {
                'binance': [self.get_all_data('binance')],
                'kraken': [self.get_all_data('kraken')]
                 }
            return Response(response_data)
        elif req_data['symbol'] == '':
            return Response({req_data['exchange']: self.get_all_data(req_data['exchange'])})
        else:
            return Response({self.get_all_data(req_data['exchange'])[req_data['symbol']]})

    @staticmethod
    def get_all_data(name):
        dict_all_data = {}
        keys = redis_instance.keys('*')
        for i in keys:
            if i.decode('utf-8').split('_')[0] == name:
                s = redis_instance.hgetall(i)
                dict_all_data[s[b'symbol'].decode('utf-8')] = s[b'price'].decode('utf-8')
        return dict_all_data

