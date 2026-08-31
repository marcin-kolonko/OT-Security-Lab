# 2026-08-31 21:09:30 by RouterOS 7.22.1
# system id = QmGtK46otgP
#
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] comment="Uplink to DMZ-FW-EDGE-01" disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] comment="Downlink to OT-RTR-DIST-01" disable-running-check=no
set [ find default-name=ether5 ] comment="Downlink to OT-SW-ACC-01 - Reserve" disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] comment="Trunk link to OT-SW-AGG-01 (Router on a stick)" disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/interface vlan
add interface=ether7 name=VLAN102-CELL02 vlan-id=102
add interface=ether7 name=VLAN103-CELL03 vlan-id=103
add interface=ether7 name=VLAN210-OT-MQTT vlan-id=210
/ip settings
set max-neighbor-entries=12288
/ipv6 settings
set max-neighbor-entries=6144 min-neighbor-entries=1536 soft-max-neighbor-entries=3072
/ip address
add address=10.250.1.1/30 interface=ether4 network=10.250.1.0
add address=10.250.30.5/28 interface=ether5 network=10.250.30.0
add address=10.251.2.1/24 interface=VLAN102-CELL02 network=10.251.2.0
add address=10.251.3.1/24 interface=VLAN103-CELL03 network=10.251.3.0
add address=10.252.10.1/26 interface=VLAN210-OT-MQTT network=10.252.10.0
add address=10.250.40.1/30 interface=ether2 network=10.250.40.0
/ip firewall filter
add action=accept chain=forward connection-state=established,related dst-address=10.251.1.11 protocol=tcp src-address=\
    10.252.10.11
add action=accept chain=forward connection-state=established,related dst-address=10.251.2.6 protocol=tcp src-address=\
    10.252.10.11
add action=accept chain=forward connection-state=established,related dst-address=10.251.3.10 protocol=tcp src-address=\
    10.252.10.11
add action=accept chain=forward connection-state=established,related dst-address=10.250.50.10 protocol=tcp src-address=\
    10.252.10.11
add action=accept chain=forward dst-address=10.252.10.11 dst-port=1883 protocol=tcp src-address=10.251.1.11
add action=accept chain=forward dst-address=10.252.10.11 dst-port=1883 protocol=tcp src-address=10.251.2.6
add action=accept chain=forward dst-address=10.252.10.11 dst-port=1883 protocol=tcp src-address=10.251.3.10
add action=accept chain=forward dst-address=10.252.10.11 dst-port=1883 protocol=tcp src-address=10.250.50.10
add action=drop chain=forward
/ip route
add dst-address=10.251.1.0/26 gateway=10.250.1.2
add dst-address=0.0.0.0/0 gateway=10.250.0.5
add dst-address=10.250.50.0/24 gateway=10.250.40.2
