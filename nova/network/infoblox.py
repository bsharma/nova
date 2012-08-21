import cStringIO as StringIO

from nova import exception
from nova import flags
from nova import log as logging
from nova.network import dhcp_driver
from nova.openstack.common import cfg
from nova import utils

LOG = logging.getLogger(__name__)

infoblox_opts = [
    cfg.StrOpt('infoblox_cli_command', default='ibcli'),
    cfg.StrOpt('infoblox_address', default=''),
    cfg.StrOpt('infoblox_user', default='admin'),
    cfg.StrOpt('infoblox_password', default='infoblox'),
]
FLAGS = flags.FLAGS
FLAGS.register_opts(infoblox_opts)


class IbcliError(Exception):
    pass


def run_ibcli(cmd):
    stdout, stderr = utils.execute(FLAGS.infoblox_cli_command,
        '-s', FLAGS.infoblox_address,
        '-u', FLAGS.infoblox_user,
        '-p', FLAGS.infoblox_password,
        '-e', cmd)
    output = StringIO.StringIO(stdout)
    res = {}
    res_list = None
    for line in output:
        if not line.startswith(' '):
            if line == '--- ---':
                if res_list is None:
                    res_list = []
                if res:
                    res_list.append(res)
                    res = {}
        else:
            k, _, v = line.partition(':')
            k, v = k.strip(), v.strip()
            res[k] = v
    if res_list is not None:
        if res:
            res_list.append(res)
        return res_list
    else:
        if 'Error' in res:
            raise IbcliError(res['Error'])
        return res


class InfobloxDHCPDriver(dhcp_driver.DHCPDriver):
    def init_network(self, ctx, network_ref):
        # TODO(yorik-sar): ensure network exists on InfoBlox
        run_ibcli('conf network add %s' % (network_ref['cidr'],))

    def teardown_network(self, ctx, network_ref):
        # TODO(yorik-sar): remove network from InfoBlox if it is not used
        if not_used:
            run_ibcli('conf network del %s' % (network_ref['cidr'],))

    def add_interface(self, ctx, network_ref, ip, vif):
        run_ibcli('conf network %s add fixed %s %s' % (network_ref['cidr'], ip,
                                                       vif['address']))

    def remove_interface(self, ctx, network_ref, ip, vif):
        run_ibcli('conf network %s del fixed %s' % (network_ref['cidr'], ip))


class InfobloxDNSDriver(object):
    """ Defines the DNS manager interface.  Does nothing. """
    def get_domains(self):
        res = run_ibcli('show zone')
        zones = []
        for line in res:
            zone_name = line.split()[0].strip()
            if '/' not in zone_name:  # NOTE(yorik-sar): filter reverse zones
                zones.append(zone_name)
        return zones

    def create_entry(self, name, address, type, domain):
        if type.lower() != 'a':
            raise exception.InvalidInput(_("This driver only supports "
                                           "type 'a'"))
        run_ibcli('conf zone %s add host %s %s' % (domain, name, address))

    def delete_entry(self, name, domain):
        run_ibcli('conf zone %s del host %s' % (domain, name))

    def modify_address(self, name, address, domain):
        run_ibcli('conf zone %s modify host %s %s' % (domain, name, address))

    def get_entries_by_address(self, address, domain):
        res = run_ibcli('show ipam address %s' % (address,))
        all_names = res.get('names', '').split()
        return [name[:-len(domain) - 1] for name in all_names
                                        if name.endswith('.' + domain)]

    def get_entries_by_name(self, name, domain):
        res = run_ibcli('show host %s.%s' % (name, domain))
        return res.get('ipv4addrs', '').split()

    def create_domain(self, fqdomain):
        run_ibcli('conf zone add %s' % (fqdomain,))

    def delete_domain(self, fqdomain):
        run_ibcli('conf zone del %s' % (fqdomain,))