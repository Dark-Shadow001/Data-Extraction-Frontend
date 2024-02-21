from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import psycopg2
from argon_drf_server.settings import DATABASES
from argon_drf_server.queryList import *
# Create your views here.


class FetchData(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = json.loads(request.body)
        filter_type = body["filter_type"]
        org_id = body["org_id"]
        channel = body["channel"]
        start_date = body["start_date"]
        end_date = body["end_date"]
        card_data = []
        chart_data = []
        table1_data = []
        table2_data = []
        wordcloud1_data = []
        wordcloud2_data = []

        try:
            connection = psycopg2.connect(user=DATABASES["default"]["USER"],
                                          password=DATABASES["default"]["PASSWORD"],
                                          host=DATABASES["default"]["HOST"],
                                          port=DATABASES["default"]["PORT"],
                                          database=DATABASES["default"]["NAME"])

            cursor = connection.cursor()
            cursor.execute(card_data_query.format(
                filter=filter_type, org_id=org_id, channel=channel, start_date=start_date, end_date=end_date))
            card_data = cursor.fetchall()
            card_col_names = [desc[0] for desc in cursor.description]

            cursor.execute(chart_data_query.format(filter=filter_type, org_id=org_id,
                           channel=channel, start_date=start_date, end_date=end_date))
            chart_data = cursor.fetchall()
            chart_col_names = [desc[0] for desc in cursor.description]

            cursor.execute(table_1_data_query.format(filter=filter_type, org_id=org_id,
                           channel=channel, start_date=start_date, end_date=end_date))
            table1_data = cursor.fetchall()
            table1_names = [desc[0] for desc in cursor.description]

            cursor.execute(table_2_data_query.format(filter=filter_type, org_id=org_id,
                           channel=channel, start_date=start_date, end_date=end_date))
            table2_data = cursor.fetchall()
            table2_names = [desc[0] for desc in cursor.description]

            cursor.execute(word_cloud_1_data_query.format(filter=filter_type, org_id=org_id,
                           channel=channel, start_date=start_date, end_date=end_date))
            wordcloud1_data = cursor.fetchall()
            word1_names = [desc[0] for desc in cursor.description]

            cursor.execute(word_cloud_2_data_query.format(filter=filter_type, org_id=org_id,
                           channel=channel, start_date=start_date, end_date=end_date))
            wordcloud2_data = cursor.fetchall()
            word2_names = [desc[0] for desc in cursor.description]

        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

            return Response({
                'card_data': {card_col_names[i]: card_data[0][i] for i in range(len(card_col_names))} if card_data else {},
                'chart_data': [{chart_col_names[i]: row[i] for i in range(len(row))} for row in chart_data[::-1]],
                'table1_data': [{table1_names[i]: row[i] for i in range(len(row))} for row in table1_data[::-1]],
                'table2_data': [{table2_names[i]: row[i] for i in range(len(row))} for row in table2_data[::-1]],
                'wordcloud1_data': [{word1_names[i]: row[i] for i in range(len(row))} for row in wordcloud1_data[::-1]],
                'wordcloud2_data': [{word2_names[i]: row[i] for i in range(len(row))} for row in wordcloud2_data[::-1]],
            })


class FetchOrganisationList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization_list = []

        try:
            connection = psycopg2.connect(user=DATABASES["default"]["USER"],
                                          password=DATABASES["default"]["PASSWORD"],
                                          host=DATABASES["default"]["HOST"],
                                          port=DATABASES["default"]["PORT"],
                                          database=DATABASES["default"]["NAME"])

            cursor = connection.cursor()
            cursor.execute(distinct_organization_query)
            organization_list = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

            return Response({
                'organization_list': organization_list
            })


class FetchProductList(APIView):
    def get(self, request):
        product_list = []
        try:
            connection = psycopg2.connect(user=DATABASES["default"]["USER"],
                                          password=DATABASES["default"]["PASSWORD"],
                                          host=DATABASES["default"]["HOST"],
                                          port=DATABASES["default"]["PORT"],
                                          database=DATABASES["default"]["NAME"])

            cursor = connection.cursor()
            cursor.execute(distinct_product_query)
            product_list_data = cursor.fetchall()
            product_list = [{'product_id': a, 'product_name': b}
                            for a, b, c, d, e in product_list_data]

        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

            return Response({
                'product_list': product_list
            })
