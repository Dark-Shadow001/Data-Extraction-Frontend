from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import psycopg2
from argon_drf_server.settings import DATABASES
from argon_drf_server.queryList import *
import json

# Create your views here.


class FetchSubscriptionData(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = json.loads(request.body)
        organization_id = body["organization_id"]
        subscription_list = []

        try:
            connection = psycopg2.connect(user=DATABASES["default"]["USER"],
                                          password=DATABASES["default"]["PASSWORD"],
                                          host=DATABASES["default"]["HOST"],
                                          port=DATABASES["default"]["PORT"],
                                          database=DATABASES["default"]["NAME"])

            cursor = connection.cursor()
            cursor.execute(subscription_query.format(organization_id=organization_id))
            subscription_list = cursor.fetchall()
            col_headers = [desc[0] for desc in cursor.description]

        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

            return Response({
                'subscription_list': [{col_headers[i]: row[i] for i in range(len(row))} for row in subscription_list]
            })
