#!/usr/bin/python3.4

import requests
import sys
import json
import time
import tempfile
import os

kube_yaml = """
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: {0}-clouduniv-1
spec:
  hosts:
  - "{1}"
  gateways:
  - {3}
  http:
  - match:
    - uri:
        prefix: /rbac
    route:
    - destination:
        port:
          number: {4}
        host: {5}
  - match:
    - uri:
        prefix: /upskill
    route:
    - destination:
        port:
          number: {6}
        host: {7}
  - match:
    - uri:
        prefix: /cu-portal-dev
    route:
    - destination:
        port:
          number: {8}
        host: {9}

"""


def get_app_info(app_config):
    for r in app_config.get('roles', []):
        if r.get('name') in ("rbac"):
            print("Waiting for RUSDN UI to get ready")
            for v in r.get('vnodes', []):
                if v.get('hostname'):
                    Frontend_Container_url = "http://{}:42621".format(v.get('network')[0]['allocated_ip'])
                    check_url(Frontend_Container_url)
            print("RUSDN UI is ready")
        if r.get('name') in ("upskill"):
            print("Waiting for upskill_Container to get ready")
            for v in r.get('vnodes', []):
                if v.get('hostname'):
                    upskill_Container_url = "http://{}:42620".format(v.get('network')[0]['allocated_ip'])
                    check_url(upskill_Container_url)
            domainname = r.get('vnodes')[0]['env']['allocated']['DOMAIN_NAME']
            print("upskill url is ready" + domainname)


def check_url(url):
    total_retries = 50
    retries = 50
    while retries > 0:
        try:
            response = requests.get(url)
        except:
            time.sleep(5)
            retries -= 1
            print("Retrying {}/{}".format(total_retries - retries, total_retries))
            if not retries:
                raise Exception("Failed to get url {}".format(url))
        else:
            break


def create_virtual_service(app_config):
    gwname = "default/service-gw"
    appname = None
    appns = None
    rbac_hostname = None
    rbac_port = "42621"
    upskill_hostname = None
    upskill_port = "42620"
    portal_hostname = None
    portal_port = "80"

    for r in app_config.get('roles', []):
        if r.get('name') in ("rbac"):
            if r.get('vnodes'):
                appname = app_config['name']
                appns = app_config['app_ns']
                hostname = r.get('vnodes')[0]['hostname']
                split_hostname = hostname.split(".")
                split_hostname[0] = "{}-ports".format(split_hostname[0])
                rbac_hostname = ".".join(split_hostname)
                domainname = r.get('vnodes')[0]['env']['allocated']['DOMAIN_NAME']
        if r.get('name') in ("upskill"):
            if r.get('vnodes'):
                hostname = r.get('vnodes')[0]['hostname']
                split_hostname = hostname.split(".")
                split_hostname[0] = "{}-ports".format(split_hostname[0])
                upskill_hostname = ".".join(split_hostname)
        if r.get('name') in ("portal"):
            if r.get('vnodes'):
                hostname = r.get('vnodes')[0]['hostname']
                split_hostname = hostname.split(".")
                split_hostname[0] = "{}-ports".format(split_hostname[0])
                portal_hostname = ".".join(split_hostname)

    if rbac_hostname:
        with tempfile.NamedTemporaryFile(delete=False) as file_object:
            file_object.write(kube_yaml.format(appname, domainname, appns, gwname, rbac_port,
                                               rbac_hostname, upskill_port, upskill_hostname, portal_port,
                                               portal_hostname).encode('utf-8'))
            file_object.flush()
            print("{}".format(kube_yaml.format(appname, domainname, appns, gwname, rbac_port,
                                               rbac_hostname, upskill_port, upskill_hostname, portal_port,
                                               portal_hostname)))
            os.system("kubectl create -f {} -n {}".format(file_object.name, appns))


def main():
    json_file = sys.argv[1]
    with open(json_file) as f:
        app_config = json.load(f)
    create_virtual_service(app_config)
    # get_app_info(app_config)


if __name__ == "__main__":
    main()