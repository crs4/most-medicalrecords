from django.http import HttpResponse
from most.web.medicalrecords.models import Configuration


def check_pyehr_conf(f):
    def wrapper(*args, **kwargs):
        try:
            pyehr_conf = Configuration.objects.get()
        except Configuration.DoesNotExist:
            return HttpResponse("Cannot find pyehr service configuration")
        url = "http://{addr}:{port}/".format(addr=pyehr_conf.ehr_service_address, port=pyehr_conf.ehr_service_port)
        kwargs["base_pyehr_url"] = url
        return f(*args, **kwargs)
    return wrapper
