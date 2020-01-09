import logging
import base64
import requests
import shutil
import re
from time import sleep

log = logging.getLogger('bender')


class RhevmAction:
    """a rhevm rest-client warpper class
   currently can registe a rhvh to rhevm
   example:
   RhevmAction("rhevm-40-1.englab.nay.redhat.com").add_new_host("10.66.8.217", "autotest01", "redhat")
   """

    auth_format = "{user}@{domain}:{password}"
    api_url = "https://{rhevm_fqdn}/ovirt-engine/api/{item}"

    headers = {
        "Prefer": "persistent-auth",
        "Accept": "application/json",
        "Content-type": "application/xml"
    }

    cert_url = ("https://{rhevm_fqdn}/ovirt-engine/services"
                "/pki-resource?resource=ca-certificate&format=X509-PEM-CA")

    rhevm_cert = "/tmp/rhevm.cert"

    def __init__(self,
                 rhevm_fqdn,
                 user="admin",
                 password="password",
                 domain="internal"):

        self.rhevm_fqdn = rhevm_fqdn
        self.user = user
        self.password = password
        self.domain = domain
        self.token = base64.b64encode(
            self.auth_format.format(
                user=self.user, domain=self.domain, password=self.password))
        self.headers.update({
            "Authorization":
            "Basic {token}".format(token=self.token)
        })
        self._get_rhevm_cert_file()
        self.req = requests.Session()

    def _get_rhevm_cert_file(self):
        r = requests.get(
            self.cert_url.format(rhevm_fqdn=self.rhevm_fqdn),
            stream=True,
            verify=False)

        if r.status_code == 200:
            with open(self.rhevm_cert, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            raise RuntimeError(
                "Can not get the cert file from %s" % self.rhevm_fqdn)

    ###################################
    # Datacenter related functions
    ###################################
    def add_datacenter(self, dc_name, is_local=False):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")

        new_dc_post_body = '''
        <data_center>
            <name>{dc_name}</name>
            <local>{is_local}</local>
        </data_center>
       '''
        body = new_dc_post_body.format(dc_name=dc_name, is_local=is_local)

        r = self.req.post(
            api_url, headers=self.headers, verify=self.rhevm_cert, data=body)

        if r.status_code != 201:
            raise RuntimeError("Failed to add new data center %s as \n%s" %
                               (dc_name, r.text))

    def remove_datacenter(self, dc_name, force=False):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")
        dc = self.list_datacenter(dc_name)

        if not dc:
            raise RuntimeError(
                "data_center %s doesn't exist, no need to remove." % dc_name)
            return

        dc_id = dc.get('id')
        api_url = api_url_base + '/{}'.format(dc_id)

        params = {'force': force}
        r = self.req.delete(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            params=params)

        if r.status_code != 200:
            raise RuntimeError("Failed to remove datacenter %s as \n%s" %
                               (dc_name, r.text))

    def list_datacenter(self, dc_name):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError(
                "Can not list datacenters from %s" % self.rhevm_fqdn)

        dcs = r.json()
        if dcs:
            for dc in dcs['data_center']:
                if dc['name'] == dc_name:
                    return dc
        else:
            return

    ##################################
    # Cluster related functions
    ##################################
    def add_cluster(self, dc_name, cluster_name, cpu_type):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="clusters")

        new_cluster_post_body = '''
        <cluster>
            <name>{cluster_name}</name>
            <cpu>
                <type>{cpu_type}</type>
            </cpu>
            <data_center>
                <name>{dc_name}</name>
            </data_center>
        </cluster>
       '''
        body = new_cluster_post_body.format(
            dc_name=dc_name, cluster_name=cluster_name, cpu_type=cpu_type)

        r = self.req.post(
            api_url, headers=self.headers, verify=self.rhevm_cert, data=body)

        if r.status_code != 201:
            raise RuntimeError("Failed to add new cluster"
                               "%s as \n%s" % (cluster_name, r.text))

    def remove_cluster(self, cluster_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="clusters")
        cluster = self.list_cluster(cluster_name)

        if not cluster:
            raise RuntimeError(
                "Cluster %s doesn't exist, no need to remove." % cluster_name)
            return

        cluster_id = cluster.get('id')
        api_url = api_url_base + '/{}'.format(cluster_id)

        r = self.req.delete(
            api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to remove cluster %s as \n%s" %
                               (cluster_name, r.text))

    def list_cluster(self, cluster_name):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="clusters")

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError(
                "Can not list clusters from %s" % self.rhevm_fqdn)

        clusters = r.json()
        if clusters:
            for cluster in clusters['cluster']:
                if cluster['name'] == cluster_name:
                    print cluster
                    return cluster
        else:
            return

    def update_cluster_cpu(self, cluster_name, cpu_type):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="clusters")
        cluster_id = self.list_cluster(cluster_name)['id']
        api_url = api_url_base + "/%s" % cluster_id

        cluster_cpu_post_body = '''
        <cluster>
            <cpu>
                <type>{cpu_type}</type>
            </cpu>
        </cluster>
        '''
        body = cluster_cpu_post_body.format(cpu_type=cpu_type)

        r = self.req.put(
            api_url, headers=self.headers, verify=self.rhevm_cert, data=body)

        if r.status_code != 200:
            raise RuntimeError("Failed to update the cpu of cluster "
                               "%s as\n%s" % (cluster_name, r.text))

    ############################################
    # Host related functions
    ############################################
    def deactive_host(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item='hosts')
        host_id = self.list_host("name", host_name)['id']
        api_url = api_url_base + "/%s/deactivate" % host_id

        r = self.req.post(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            data="<action/>")
        ret = r.json()
        print ret
        if ret['status'] != 'complete':
            raise RuntimeError(ret['fault']['detail'])

    def add_host(self, ip, host_name, password, cluster_name='Default', deploy_hosted_engine=False):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")

        new_host_post_body = '''
        <host>
            <name>{host_name}</name>
            <address>{ip}</address>
            <root_password>{password}</root_password>
            <cluster>
              <name>{cluster_name}</name>
            </cluster>
        </host>
       '''
        body = new_host_post_body.format(
            host_name=host_name,
            ip=ip,
            password=password,
            cluster_name=cluster_name)

        params = {'deploy_hosted_engine': deploy_hosted_engine}

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert, params=params)

        if r.status_code != 201:
            raise RuntimeError("Failed to add new host "
                               "%s as\n%s" % (host_name, r.text))

    def remove_host(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host = self.list_host(key="name", value=host_name)

        if host:
            host_id = host.get('id')

            if host.get('status') != 'maintenance':
                self.deactive_host(host_id)
                sleep(10)

            api_url = api_url_base + '/%s' % host_id

            r = self.req.delete(
                api_url,
                headers=self.headers,
                verify=self.rhevm_cert,
                params={"async": "false"})

            if r.status_code != 200:
                raise RuntimeError("Delete host %s failed as\n%s" % (host_name,
                                                                     r.text))
        else:
            raise RuntimeError(
                "Host %s doesn't exist, no need to delete." % host_name)

    def list_host(self, key=None, value=None):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Can not list hosts from %s" % self.rhevm_fqdn)

        hosts = r.json()
        
        if hosts:
            for host in hosts['host']:
                if host.get(key) == value:
                    return host
        else:
            return None

    def get_host_status(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host = self.list_host(key="name", value=host_name)

        if host:
            return host.get('status')

    def get_host_id(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host = self.list_host(key="name", value=host_name)
        if host:
            return host.get('id')

    def update_available_check(self, host_id):
        rhvm_version = self.rhevm_fqdn.split('-')[0]

        if rhvm_version == "rhvm42" or rhvm_version == "rhvm41":
            api_url_base = self.api_url.format(
                rhevm_fqdn=self.rhevm_fqdn, item="hosts")
            api_url = api_url_base + '/%s' % host_id + '/upgradecheck'

            r = self.req.post(
                api_url,
                data="<action/>",
                headers=self.headers,
                verify=self.rhevm_cert,
                params={"async": "false"})

            if r.status_code != 200:
                raise RuntimeError(
                    "Failed to execute upgradecheck, r.status_code is %d." %
                    r.status_code)

        count_max = 13
        sleep_time = 300
        if rhvm_version == "rhvm42" or rhvm_version == "rhvm41":
            count_max = 10
            sleep_time = 30

        count = 0
        while (count < count_max):
            sleep(sleep_time)
            update_available = self.list_host(
                key="id", value=host_id)['update_available']
            if update_available == 'true':
                break
            count = count + 1
        else:
            raise RuntimeError("update is not available.")
            return False

        return True

    def get_host_events(self, host_name):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="events")

        params = {'search': "event_host={}".format(host_name)}
        r = self.req.get(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            params=params)

        if r.status_code != 200:
            raise RuntimeError("Can not list events of host %s on %s" %
                               (host_name, self.rhevm_fqdn))
            return None
        else:
            return r.json()

    def get_host_event_by_des(self, host_name, description):
        events = self.get_host_events(host_name)
        if events:
            for event in events.get('event'):
                if description in event.get('description'):
                    return True
            else:
                return False
        else:
            return False

    def del_host_events(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="events")
        events = self.get_host_events(host_name)
        if events:
            for event in events.get('event'):
                event_id = event.get('id')
                api_url = api_url_base + '/%s' % event_id
                r = self.req.delete(
                    api_url,
                    headers=self.headers,
                    verify=self.rhevm_cert,
                    params={"async": "false"})
                if r.status_code != 200:
                    raise RuntimeError(
                        "Failed to delete events of host %s as\n %s" %
                        (host_name, r.text))
        else:
            raise RuntimeError(
                "Host %s events doesn't exist, no need to delete." % host_name)

    def upgrade_host(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host = self.list_host(key="name", value=host_name)

        if host:
            host_id = host.get('id')

            # check host update available
            if not self.update_available_check(host_id):
                raise RuntimeError(
                    "Update is not available for host %s" % host_name)
            # try to trigger upgrade
            api_url = api_url_base + '/%s' % host_id + '/upgrade'
            count = 0
            while (count < 3):
                r = self.req.post(
                    api_url,
                    headers=self.headers,
                    verify=self.rhevm_cert,
                    data="<action/>",
                    params={"async": "false"})
                if r.status_code == 200:
                    break
                count = count + 1
            else:
                raise RuntimeError(
                    "Failed to execute upgrade on host %s" % host_name)

            # check upgrade status
            description = 'Host {} upgrade was completed successfully'.format(
                host_name)
            count = 0
            while (count < 4):
                sleep(300)
                if self.get_host_event_by_des(host_name, description):
                    log.info(description)
                    break
                count = count + 1
            else:
                raise RuntimeError("Upgrade host %s failed." % host_name)
        else:
            raise RuntimeError("Can't find host with name %s" % host_name)

    def check_update_available(self, host_name):
        host = self.list_host(key="name", value=host_name)

        if host:
            host_id = host.get('id')

            # check host update available
            if not self.update_available_check(host_id):
                return False
            else:
                return True

    ######################################
    # Storage related functions
    ######################################
    def add_plain_storage_domain(self, domain_name, domain_type, storage_type,
                                 storage_addr, storage_path, host):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="storagedomains")

        storage_domain_post_body = '''
        <storage_domain>
            <name>{domain_name}</name>
            <type>{domain_type}</type>
            <storage>
                <type>{storage_type}</type>
                <address>{storage_addr}</address>
                <path>{storage_path}</path>
            </storage>
            <host>
                <name>{host}</name>
            </host>
        </storage_domain>
        '''
        body = storage_domain_post_body.format(
            domain_name=domain_name,
            domain_type=domain_type,
            storage_type=storage_type,
            storage_addr=storage_addr,
            storage_path=storage_path,
            host=host)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to add new storage domain"
                               "%s as\n%s" % (domain_name, r.text))

    def add_fc_scsi_storage_domain(self, sd_name, sd_type, storage_type,
                                   lun_id, host):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="storagedomains")
        storage_domain_post_body = '''
        <storage_domain>
          <name>{sd_name}</name>
          <type>{sd_type}</type>
          <storage>
            <type>{storage_type}</type>
            <logical_units>
              <logical_unit id="{lun_id}"/>
            </logical_units>
          </storage>
          <host>
            <name>{host}</name>
          </host>
        </storage_domain>
        '''
        body = storage_domain_post_body.format(
            sd_name=sd_name,
            sd_type=sd_type,
            storage_type=storage_type,
            lun_id=lun_id,
            host=host)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create storage domain "
                               "%s as\n%s" % (sd_name, r.text))

    # The function don't work , no resources about host_storage.
    def list_host_storage(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")

        host_id = self.list_host("name", host_name).get('id')
        api_url = api_url_base + '/{}'.format(host_id) + '/storages'

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list the stroges of host "
                               "%s as\n%s" % (host_name, r.text))

        return r.json()

    def list_dc_storage(self, dc_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")

        dc_id = self.list_datacenter(dc_name)['id']
        api_url = api_url_base + '/{}'.format(dc_id) + '/storagedomains'

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list the storagedomains of"
                               " %s as\n%s" % (dc_name, r.text))
        sds = r.json()

        sd_list = []
        master_type = []

        if sds:
            for sd in sds['storage_domain']:
                sd_list.append(sd.get('name'))
                master_type.append(sd.get('master'))

        #return dict(zip(sd_list, master_type))
        return dict(map(lambda x,y:[x,y], sd_list, master_type))

    def attach_sd_to_datacenter(self, sd_name, dc_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")
        dc_id = self.list_datacenter(dc_name)['id']
        api_url = api_url_base + '/%s/storagedomains' % dc_id

        new_storage_post_body = '''
        <storage_domain>
            <name>{storage_name}</name>
        </storage_domain>
       '''
        body = new_storage_post_body.format(storage_name=sd_name)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError(
                "Failed to attach storage %s to datacenter %s as\n %s" %
                (sd_name, dc_name, r.text))

    def list_storage_domain(self, sd_name):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="storagedomains")

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list storage domain "
                               "%s as\n%s" % (sd_name, r.text))

        sds = r.json()
        if sds:
            for sd in sds['storage_domain']:
                if sd['name'] == sd_name:
                    return sd
        else:
            return

    def remove_storage_domain(self, sd_name, host_name, destroy=True):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="storagedomains")

        sd_id = self.list_storage_domain(sd_name)['id']
        api_url = api_url_base + '/{}'.format(sd_id)

        params = {'destroy': destroy, 'host': host_name}
        r = self.req.delete(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            params=params)

        if r.status_code != 200:
            raise RuntimeError("Failed to remove storage domain "
                               "%s as\n%s" % (sd_name, r.text))

    ##########################################
    # VM related functions
    ##########################################
    def create_vm(self, vm_name, tpl_name="Blank", cluster_name="default"):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        new_vm_body = '''
        <vm>
            <name>{vm_name}</name>
            <description>{vm_name}</description>
            <cluster>
                <name>{cluster_name}</name>
            </cluster>
            <template>
                <name>{tpl_name}</name>
            </template>
        </vm>
       '''
        body = new_vm_body.format(
            vm_name=vm_name, cluster_name=cluster_name, tpl_name=tpl_name)

        r = self.req.post(
            api_url_base,
            data=body,
            headers=self.headers,
            verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create virtual machine")
        else:
            return r.json()["id"]

    def list_vm(self, vm_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        r = self.req.get(
            api_url_base, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list vm "
                               "%s as\n%s" % (vm_name, r.text))

        vms = r.json()
        if vms:
            for vm in vms['vm']:
                if vm['name'] == vm_name:
                    return vm
        else:
            return

    def start_vm(self, vm_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/%s/start' % vm_id

        vm_action = '''
        <action>
            <vm>
                <os>
                    <boot>
                        <devices>
                            <device>hd</device>
                        </devices>
                    </boot>
                </os>
            </vm>
        </action>
       '''
        r = self.req.post(
            api_url,
            data=vm_action,
            headers=self.headers,
            verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to start vm "
                               "%s as\n%s" % (vm_name, r.text))

    def operate_vm(self, vm_name, operation):
        normal_operations = ['reboot', 'shutdown', 'stop', 'suspend']
        if operation not in normal_operations:
            raise RuntimeError(
                "Only support operations ['reboot', 'shutdown', 'stop', 'suspend']"
            )

        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/%s/%s' % (vm_id, operation)

        vm_action = '''
        <action/>
        '''
        r = self.req.post(
            api_url,
            data=vm_action,
            headers=self.headers,
            verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to %s vm "
                               "%s as\n%s" % (operation, vm_name, r.text))

    def migrate_vm(self, vm_name, dest_host_fqdn):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/%s/migrate' % vm_id
        # host_id = self.get_host_id('cockpit-vm')
        host_id = self.get_host_id(dest_host_fqdn)
        
        vm_action = ('''
        <action>
            <host id="%s"/>    
        </action>
        ''' %host_id)
        
        r = self.req.post(
            api_url,
            data=vm_action,
            headers=self.headers,
            verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to migrate vm %s as\n%s" % (vm_name, r.text))

    def remove_vm(self, vm_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/%s' % vm_id

        r = self.req.delete(
            api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to remove vm "
                               "%s as\n%s" % (vm_name, r.text))

    def create_vm_image_disk(self, vm_name, sd_name, disk_name, disk_size):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/{}'.format(vm_id) + '/diskattachments'

        attach_disk_post_body = '''
        <disk_attachment>
          <bootable>true</bootable>
          <interface>virtio</interface>
          <active>true</active>
          <disk>
            <format>cow</format>
            <name>{disk_name}</name>
            <provisioned_size>{disk_size}</provisioned_size>
            <storage_domains>
              <storage_domain>
                <name>{sd_name}</name>
              </storage_domain>
            </storage_domains>
          </disk>
        </disk_attachment>
        '''

        body = attach_disk_post_body.format(
            disk_name=disk_name, disk_size=disk_size, sd_name=sd_name)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create image disk for vm "
                               "%s as\n%s" % (vm_name, r.text))

    def create_vm_direct_lun_disk(self,
                                  vm_name,
                                  disk_name,
                                  host_name,
                                  lun_type,
                                  lun_id,
                                  lun_addr="",
                                  lun_port="",
                                  lun_target=""):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        host_id = self.list_host(host_name)['id']
        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/{}'.format(vm_id) + '/diskattachments'

        if lun_type == "iscsi":
            attach_disk_post_body = '''
            <disk_attachment>
              <bootable>false</bootable>
              <interface>virtio</interface>
              <active>true</active>
                <disk>
                  <alias>{disk_name}</alias>
                  <lun_storage>
                    <host id="{host_id}"/>
                    <type>{lun_type}</type>
                    <logical_units>
                      <logical_unit id="{lun_id}">
                        <address>{lun_addr}</address>
                        <port>{lun_port}</port>
                        <target>{lun_target}</target>
                      </logical_unit>
                    </logical_units>
                  </lun_storage>
                </disk>
            </disk_attachment>
            '''
            body = attach_disk_post_body.format(
                disk_name=disk_name,
                host_id=host_id,
                lun_type=lun_type,
                lun_id=lun_id,
                lun_addr=lun_addr,
                lun_port=lun_port,
                lun_target=lun_target)
        else:
            attach_disk_post_body = '''
            <disk_attachment>
              <bootable>false</bootable>
              <interface>virtio</interface>
              <active>true</active>
                <disk>
                  <alias>{disk_name}</alias>
                  <lun_storage>
                    <host id="{host_id}"/>
                    <type>{lun_type}</type>
                    <logical_units>
                      <logical_unit id="{lun_id}"/>
                    </logical_units>
                  </lun_storage>
                </disk>
            </disk_attachment>
            '''
            body = attach_disk_post_body.format(
                disk_name=disk_name,
                host_id=host_id,
                lun_type=lun_type,
                lun_id=lun_id)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create lun disk for vm "
                               "%s as\n%s" % (vm_name, r.text))

    def list_vm_disk_attachments(self, vm_name, disk_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")
        vm_id = self.list_vm(vm_name)['id']
        api_url = api_url_base + '/{}'.format(vm_id) + '/diskattachments'

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list disk %s of "
                               "%s as\n%s" % (disk_name, vm_name, r.text))

        diskattachment = r.json()
        if diskattachment:
            disk_id = self.list_disk(disk_name)['id']
            for disk in diskattachment['disk_attachment']:
                if disk['id'] == disk_id:
                    return disk
        else:
            return

    ##########################################
    # Network related functions
    ##########################################
    def list_network(self, dc_name, nw_name):
        api_url = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="networks")
        dc_id = self.list_datacenter(dc_name).get('id')

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)
        if r.status_code != 200:
            raise RuntimeError(
                "Can not list networks from %s" % self.rhevm_fqdn)

        networks = r.json()
        if networks:
            for network in networks.get('network'):
                if network.get('name') == nw_name and network.get(
                        'data_center').get('id') == dc_id:
                    return network
        else:
            return

    def update_network(self,
                       dc_name,
                       param_name,
                       param_value,
                       nw_name="ovirtmgmt"):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="networks")
        network = self.list_network(dc_name, nw_name)

        if not network:
            raise RuntimeError("Can't find network %s in data center %s" %
                               (nw_name, dc_name))

        network_id = network.get('id')
        api_url = api_url_base + '/%s' % network_id

        if param_name == "vlan":
            update_network_body = '''
            <network>
                <vlan id="{value}"/>
            </network>
            '''
        else:
            update_network_body = '''
            <network>
                <{key}>{value}</{key}>
            </network>
            '''

        body = update_network_body.format(key=param_name, value=param_value)

        r = self.req.put(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            data=body,
            params={"async": "false"})

        if r.status_code != 200:
            raise RuntimeError(
                "Update network %s with %s=%s in data center %s failed as\n %s"
                % (nw_name, param_name, param_value, dc_name, r.text))

    def update_dc_network(self, dc_name, network_name, key, value):
        """
        Update the network of the datacenter
        key: [name, description, ip, vlan, stp, display]
        """
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")
        dc_id = self.list_datacenter(dc_name)['id']
        network_id = self.list_network(dc_name, network_name)['id']
        api_url = api_url_base + "/%s" % dc_id + "/networks/%s" % network_id

        if key == "vlan":
            dc_network_post_body = '''
            <network>
              <vlan id="{value}"/>
            </network>
            '''
        else:
            dc_network_post_body = '''
            <network>
              <{key}>{value}</{key}>
            </network>
            '''
        body = dc_network_post_body.format(key=key, value=value)

        r = self.req.put(
            api_url, headers=self.headers, verify=self.rhevm_cert, data=body)
        if r.status_code != 200:
            raise RuntimeError("Failed to update the network of "
                               "%s as\n%s" % (dc_name, r.text))

    ##########################################
    # Disk related functions
    # https://rhvm41-vlan50-1.lab.eng.pek2.redhat.com/ovirt-engine/apidoc/#services-disks
    ##########################################
    def create_float_image_disk(self, sd_name, disk_name, disk_size):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="disks")

        new_disk_post_body = '''
        <disk>
          <storage_domains>
            <storage_domain id="{sd_id}"/>
          </storage_domains>
          <name>{disk_name}</name>
          <provisioned_size>{disk_size}</provisioned_size>
          <format>cow</format>
        </disk>
        '''
        sd_id = self.list_storage_domain(sd_name)['id']
        body = new_disk_post_body.format(
            sd_id=sd_id, disk_name=disk_name, disk_size=disk_size)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create float image disk "
                               "%s as\n%s" % (disk_name, r.text))

    def create_float_direct_lun_disk(self,
                                     disk_name,
                                     host_name,
                                     lun_type,
                                     lun_id,
                                     lun_addr="",
                                     lun_port="",
                                     lun_target=""):
        #
        # lun_type = {'iscsi', 'fcp', 'nfs', 'localfs', 'posixfs',
        # 'glusterfs', 'glance', 'cinder'}
        #
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="disks")

        new_disk_post_body = '''
        <disk>
          <alias>{disk_name}</alias>
          <lun_storage>
            <host id="{host_id}"/>
            <type>{lun_type}</type>
            <logical_units>
              <logical_unit id="{lun_id}">
                <address>{lun_addr}</address>
                <port>{lun_port}</port>
                <target>{lun_target}</target>
              </logical_unit>
            </logical_units>
          </lun_storage>
        </disk>
        '''
        host_id = self.list_host(host_name)['id']
        body = new_disk_post_body.format(
            disk_name=disk_name,
            host_id=host_id,
            lun_type=lun_type,
            lun_id=lun_id,
            lun_addr=lun_addr,
            lun_port=lun_port,
            lun_target=lun_target)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to create float lun disk "
                               "%s as\n%s" % (disk_name, r.text))

    def attach_disk_to_vm(self, disk_name, vm_name, bootable=False):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="vms")

        vm_id = self.list_vm(vm_name)['id']
        disk_id = self.list_disk(disk_name)['id']

        api_url = api_url_base + '/{}'.format(vm_id) + '/diskattachments'

        attach_disk_post_body = '''
        <disk_attachment>
          <bootable>{bootable}</bootable>
          <interface>ide</interface>
          <active>true</active>
          <disk id="{disk_id}"/>
        </disk_attachment>
        '''

        body = attach_disk_post_body.format(disk_id=disk_id, bootable=bootable)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            raise RuntimeError("Failed to attach disk %s to "
                               "%s as\n%s" % (disk_name, vm_name, r.text))

    def list_disk(self, disk_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="disks")

        r = self.req.get(
            api_url_base, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list disk "
                               "%s as\n%s" % (disk_name, r.text))

        disks = r.json()
        if disks:
            for disk in disks['disk']:
                if disk['name'] == disk_name:
                    return disk
        else:
            return

    def list_template(self, template_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="templates")

        r = self.req.get(
            api_url_base, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list template "
                               "%s as\n%s" % (template_name, r.text))

        templates = r.json()
        if templates:
            for template in templates['template']:
                if template['name'] == template_name:
                    return template
        else:
            return

    def get_vm_ovirt_info_on_engine(self, vm_name):
        vm_ovirt_info = {}
        try:
            vm_ovirt_info['ovirt-description'] = self.list_vm(vm_name)['description']
        except Exception as e:
            vm_ovirt_info['ovirt-description'] = ''
        vm_ovirt_info['ovirt-ostype'] = self.list_vm(vm_name)['os']['type']
        # vm_ha: false-> disabled, vm_stateless : false -> no
        vm_ovirt_info['ovirt-ha'] = self.list_vm(vm_name)['high_availability']['enabled']
        vm_ovirt_info['ovirt-stateless'] = self.list_vm(vm_name)['stateless']
        vm_ovirt_info['ovirt-optimizedfor'] = self.list_vm(vm_name)['type']
        vm_ovirt_info['vm-status'] = self.list_vm(vm_name)['status']
        vm_ovirt_info['cores'] = self.list_vm(vm_name)['cpu']['topology']['cores']
        vm_ovirt_info['sockets'] = self.list_vm(vm_name)['cpu']['topology']['sockets']
        vm_ovirt_info['threads'] = self.list_vm(vm_name)['cpu']['topology']['threads']
        try:
            vm_ovirt_info['host_id'] = self.list_vm(vm_name)['host']['id']
        except Exception as e:
            vm_ovirt_info['host_id'] = ''
        return vm_ovirt_info

    def get_template_info_on_engine(self, template_name):
        template_info = {}
        template_info['name'] = self.list_template(template_name)['name']
        template_info['version'] = self.list_template(template_name)['version']['version_name']
        template_info['description'] = self.list_template(template_name)['description']
        # base template id
        template_info['base-template'] = self.list_template(template_name)['version']['base_template']['id']
        # memory 1024*1024*1024  1G
        template_info['memory'] = self.list_template(template_name)['memory']
        template_info['vcpus'] = self.list_template(template_name)['cpu']['topology']['cores']
        template_info['os'] = self.list_template(template_name)['os']['type']
        # false
        template_info['ha'] = self.list_template(template_name)['high_availability']['enabled']
        # false
        template_info['stateless'] = self.list_template(template_name)['stateless']

        return template_info

    def get_vm_icon_data(self, vm_name):
        vm_icon_id = self.list_vm(vm_name)['large_icon']['id']

        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="icons")

        r = self.req.get(
            api_url_base, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 200:
            raise RuntimeError("Failed to list template "
                               "%s as\n%s" % (template_name, r.text))

        icons = r.json()
        if icons:
            for icon in icons['icon']:
                if icon['id'] == vm_icon_id:
                    return icon['data']
        else:
            return


if __name__ == '__main__':
    rhvm = RhevmAction("rhvm42-vlan50-1.lab.eng.pek2.redhat.com")
    #rhvm._get_rhevm_cert_file()
    rhvm.add_datacenter("yzhao_dc_intel")
    rhvm.add_cluster("yzhao_dc_intel", "yzhao_intel", "Intel")
    rhvm.add_host("10.66.8.176", "yzhao_intel_rhel", "redhat")
