import csv
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.iot_server.models import DataSource, DataValue, init_api_token_str


# Create your views here.
class WeatherDashView(View):
    def get(self, request):
        temp_data = []
        humid_data = []

        source = DataSource.objects.get(name="Local AHT20")
        temperature_values = DataValue.objects.filter(source=source, value__type="temperature").order_by("-id")[:10]
        humidity_values = DataValue.objects.filter(source=source, value__type="humidity").order_by("-id")[:10]

        for _ in temperature_values:
            temp_data.append(round(_.value['value'], 1))

        for _ in humidity_values:
            humid_data.append(round(_.value['value'], 1))

        return render(request, "iot_server/temperature_humidity_dash.html", {
            "temp_data": json.dumps(temp_data),
            "humid_data": json.dumps(humid_data)
        })


@method_decorator(csrf_exempt, name='dispatch')
class PostDataView(View):
    # def get(self, request):
    #     return HttpResponse("HELLO?!?!")
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        request_data = json.loads(body_unicode)
        print(request_data)
        if 'data_source_token' not in request_data:
            return JsonResponse({"success": False, 'error': "Missing Required Field 'data_source_token'"}, status=400)

        if 'data_value' not in request_data:
            return JsonResponse({"success": False, 'error': "Missing Required Field 'data_value'"}, status=400)

        request_token = request_data['data_source_token']

        try:
            data_source = DataSource.objects.get(token=request_token)
            print("found:")
            print(data_source)

            new_data_value = DataValue(
                source=data_source,
                value=request_data['data_value'],
                user=data_source.user
            )
            new_data_value.save()
            return JsonResponse({"success": True})
        except DataSource.DoesNotExist:
            return JsonResponse({"success": False, 'error': "Data Source Not Found"}, status=404)


class ListDataSources(View):
    def get(self, request):
        data_sources = DataSource.objects.filter(user=request.user)
        return render(request, 'iot_server/list_data_sources.html', {"data_sources": data_sources})

class NewDataSource(View):
    def get(self, request):
        return render(request, 'iot_server/new_data_source.html', {})

    def post(self, request):
        new_name = request.POST.get("name", None)
        local = request.POST.get("local", False)

        new_data_source = DataSource(
            name=new_name,
            local=local,
            user=request.user
        )
        new_data_source.save()
        return redirect(reverse('list_data_sources'))
class DataSourceDetail(View):
    def get(self, request, data_source_id):

        type_filter = request.GET.get("type_filter", None)

        try:
            data_source = DataSource.objects.get(id=data_source_id, user=request.user)
            if not type_filter:
                data_values = DataValue.objects.filter(source=data_source, user=request.user).order_by("-created_at")[
                              :10]
            else:
                data_values = DataValue.objects.filter(source=data_source, user=request.user,
                                                       value__type=type_filter).order_by("-created_at")[:10]

            value_types = DataValue.objects.values_list(
                "value__type").distinct()
            return render(request, 'iot_server/data_source_detail.html', {
                "type_filter": type_filter,
                "data_source": data_source,
                "value_types": value_types,
                "data_values": data_values
            })
        except DataSource.DoesNotExist:
            return render(request, 'iot_server/not_found.html', {})


class DownloadDataValues(View):
    def get(self, request, data_source_id):
        type_filter = request.GET.get("type_filter", None)
        try:
            data_source = DataSource.objects.get(id=data_source_id, user=request.user)
            if not type_filter:
                data_values = DataValue.objects.filter(source=data_source, user=request.user).order_by("-created_at")
            else:
                data_values = DataValue.objects.filter(source=data_source, user=request.user, value__type=type_filter).order_by("-created_at")

            response = HttpResponse(
                content_type="text/csv",
                headers={
                    f"Content-Disposition": f'attachment; filename="{data_source.name} Data {timezone.now().strftime("%m-%d-%Y %H-%M-%S")}.csv"'},
            )

            writer = csv.writer(response)
            writer.writerow(["Timestamp", "Type", "Value", "Unit"])
            for value in data_values:
                writer.writerow([value.created_at, value.value['type'], value.value['value'], value.value['unit']])

            return response
        except DataSource.DoesNotExist:
            return render(request, 'iot_server/not_found.html', {})

class RefreshDataSourceToken(View):
    def post(self, request, data_source_id):
        try:
            data_source = DataSource.objects.get(id=data_source_id, user=request.user)
            data_source.token = init_api_token_str()
            data_source.save()

            return JsonResponse({"success": True})
        except DataSource.DoesNotExist:
            return JsonResponse({"success": False, 'error': 'Data Source Not Found'}, status=404)