import re
import os
import time
import logging
import commands
import subprocess

"""
This function is used to clean the previous HostedEngine environment, \
then you can redeploy HostedEngine again
"""

log = logging.getLogger("bender")


try:
    log.info("-=== Destroy hosted-engine VM ===-")
    subprocess.call("hosted-engine  --vm-poweroff", shell=True)
    time.sleep(3)

    log.info("-=== Destroy the VMs ===-")
    (value, host) = commands.getstatusoutput("vdsm-client Host getVMList")
    pattern = re.compile('"(.*)"')
    hostlist = pattern.findall(host)
    for i in hostlist:
        os.system("vdsm-client VM destroy vmID=%s" % i)

    time.sleep(5)

    log.info("-=== Stop HA services ===-")
    subprocess.call("systemctl stop ovirt-ha-agent ovirt-ha-broker", shell=True)

    time.sleep(5)

    log.info("-=== Shutdown sanlock ===-")
    subprocess.call("sanlock client shutdown -f 1", shell=True)

    log.info("-=== Disconnecting the hosted-engine storage domain ===-")
    subprocess.call("hosted-engine --disconnect-storage", shell=True)

    log.info("-=== Re-configure VDSM networks ===-")
    subprocess.call("vdsm-tool restore-nets", shell=True)

    log.info("-=== Stop other services ===-")
    subprocess.call("systemctl stop vdsmd supervdsmd libvirtd momd sanlock", shell=True)

    log.info("-=== Re-configure external daemons ===-")
    subprocess.call("vdsm-tool remove-config", shell=True)

except Exception as e:
    log.exception(e)

finally:
    log.info("-=== Removing configuration files ===-")
    subprocess.call("rm -rf /etc/init/libvirtd.conf \
                    /etc/libvirt/nwfilter/vdsm-no-mac-spoofing.xml \
                    /etc/ovirt-hosted-engine/answers.conf \
                    /etc/ovirt-hosted-engine/hosted-engine.conf /etc/vdsm/vdsm.conf \
                    /etc/pki/vdsm/*/*.pem /etc/pki/CA/cacert.pem /etc/pki/libvirt/*.pem \
                    /etc/pki/libvirt/private/*.pem /etc/pki/ovirt-vmconsole/*.pem \
                    /var/cache/libvirt/* /var/run/ovirt-hosted-engine-ha/*", shell=True)

    log.info("-=== Finish cleaning the SHE ENV ===-")

