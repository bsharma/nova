<?xml version='1.0' encoding='UTF-8'?>
<servers xmlns:OS-EXT-SRV-ATTR="http://docs.openstack.org/compute/ext/extended_status/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1">
  <server xmlns:OS-EXT-SRV-ATTR="http://docs.openstack.org/compute/ext/extended_status/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1" status="ACTIVE" updated="%(timestamp)s" hostId="%(hostid)s" name="new-server-test" created="%(timestamp)s" userId="fake" tenantId="openstack" accessIPv4="" accessIPv6="" progress="0" id="%(id)s" OS-EXT-SRV-ATTR:instance_name="%(instance_name)s" OS-EXT-SRV-ATTR:host="%(compute_host)s" OS-EXT-SRV-ATTR:hypervisor_hostname="None">
    <image id="%(uuid)s">
      <atom:link href="%(host)s/openstack/images/%(uuid)s" rel="bookmark"/>
    </image>
    <flavor id="1">
      <atom:link href="%(host)s/openstack/flavors/1" rel="bookmark"/>
    </flavor>
    <metadata>
      <meta key="My Server Name">Apache1</meta>
    </metadata>
    <addresses>
      <network id="private">
        <ip version="4" addr="%(ip)s"/>
      </network>
    </addresses>
    <atom:link href="%(host)s/v2/openstack/servers/%(id)s" rel="self"/>
    <atom:link href="%(host)s/openstack/servers/%(id)s" rel="bookmark"/>
  </server>
</servers>