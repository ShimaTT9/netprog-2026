import sys
import time

from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

AP_RANGE = int(sys.argv[1]) if len(sys.argv) > 1 else 35
MANUAL = len(sys.argv) > 2 and sys.argv[2] == 'manual'

AP_INFO = {'ap1': ('netprog-ap1', 20.0), 'ap2': ('netprog-ap2', 80.0)}


def get_assoc(sta):
    """AP name sta is associated with (Mininet-WiFi attribute), or None."""

    assoc = sta.params.get('associatedTo')
    if assoc is None:
        try:
            assoc = sta.wintfs[0].associatedTo
        except (AttributeError, IndexError, KeyError):
            assoc = None
    if isinstance(assoc, list):
        assoc = assoc[0] if assoc else None
    if assoc is None:
        return None
    if hasattr(assoc, 'node'):
        return assoc.node.name
    return getattr(assoc, 'name', str(assoc))


def get_link_ssid(sta):
    out = sta.cmd('iw dev %s-wlan0 link' % sta.name)
    for line in out.splitlines():
        if 'SSID:' in line:
            return line.split('SSID:')[1].strip()
    return None


def x_of(sta):
    try:
        return float(sta.position[0])
    except Exception:
        return None


def manual_assoc(sta):
    """Fallback: stay on current AP while in range, else join nearest in range."""
    x = x_of(sta)
    if x is None:
        return
    in_range = {ap: abs(x - apx) for ap, (_, apx) in AP_INFO.items()
                if abs(x - apx) <= AP_RANGE}
    cur_ssid = get_link_ssid(sta)
    cur_ap = next((ap for ap, (s, _) in AP_INFO.items() if s == cur_ssid), None)
    if cur_ap in in_range:
        return                                  # still in range: keep it
    if cur_ap is not None:
        sta.cmd('iw dev %s-wlan0 disconnect' % sta.name)
    if in_range:
        best = min(in_range, key=in_range.get)
        sta.cmd('iw dev %s-wlan0 connect %s' % (sta.name, AP_INFO[best][0]))


def topology():
    net = Mininet_wifi()

    info("* Creating nodes (AP range = %s)\n" % AP_RANGE)
    sta1 = net.addStation('sta1', position='15,50,0')   # 10.0.0.1
    sta2 = net.addStation('sta2', position='85,50,0')   # 10.0.0.2
    sta3 = net.addStation('sta3', position='10,50,0')   # mobile station
    # failMode='standalone': no OpenFlow controller in this VM, so the APs
    # must act as normal learning switches or they drop all traffic.
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap1', mode='g', channel='1',
                             position='20,50,0', range=AP_RANGE,
                             failMode='standalone')
    ap2 = net.addAccessPoint('ap2', ssid='netprog-ap2', mode='g', channel='6',
                             position='80,50,0', range=AP_RANGE,
                             failMode='standalone')

    info("* Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.addLink(ap1, ap2)               # wired backbone

    # Mobility must be configured BEFORE net.build() in this Mininet-WiFi
    # version; otherwise sta3 never moves (position stays at 10,50,0).
    info("* Configuring mobility\n")
    net.startMobility(time=0)
    # TODO 2 / TODO 3: walk from x=10 to x=90 between t=1 and t=20
    net.mobility(sta3, 'start', time=1, position='10,50,0')
    net.mobility(sta3, 'stop', time=20, position='90,50,0')
    net.stopMobility(time=21)

    info("* Starting network\n")
    net.build()
    net.start()

    # Static stations did not auto-associate in this VM -> connect explicitly
    sta1.cmd('iw dev sta1-wlan0 connect netprog-ap1')
    sta2.cmd('iw dev sta2-wlan0 connect netprog-ap2')
    if MANUAL:
        sta3.cmd('iw dev sta3-wlan0 connect netprog-ap1')

    # Part E: background ping sta3 -> sta1 every 0.5 s
    sta3.cmd('ping -i 0.5 10.0.0.1 > /tmp/sta3_ping.log &')

    info("* Monitoring sta3 association during mobility\n")
    for t in range(22):
        if MANUAL:
            manual_assoc(sta3)
        assoc = get_assoc(sta3)
        x = x_of(sta3)
        xs = f"{x:5.1f}" if x is not None else "  ?"
        print(f"t={t}s sta3 associated to: {assoc}   "
              f"(x={xs}, iw link SSID={get_link_ssid(sta3)})")
        time.sleep(1)

    CLI(net)
    sta3.cmd('pkill -f "ping -i 0.5"')
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
