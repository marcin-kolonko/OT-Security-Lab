# 2026-08-31 20:49:09 by RouterOS 7.22.1
# system id = /LyX9R3CPkB
#
/interface ethernet
set [ find default-name=ether1 ] comment="OT Zone - Uplink to OT-RTR-CORE-01" disable-running-check=no
set [ find default-name=ether2 ] comment="OT Zone - Link to Industrial Switch CELL01" disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/ip settings
set max-neighbor-entries=12288
/ipv6 settings
set max-neighbor-entries=6144 min-neighbor-entries=1536 soft-max-neighbor-entries=3072
/ip address
add address=10.250.1.2/30 interface=ether1 network=10.250.1.0
add address=10.251.1.1/26 interface=ether2 network=10.251.1.0
/ip firewall filter
add action=accept chain=forward connection-state=established,related dst-address=10.251.1.11 protocol=tcp src-address=\
    10.252.10.11
add action=accept chain=forward dst-address=10.252.10.11 dst-port=1883 protocol=tcp src-address=10.251.1.11
add action=drop chain=forward
/ip route
add dst-address=10.250.0.0/24 gateway=10.250.1.1
add dst-address=10.250.30.0/28 gateway=10.250.1.1
add dst-address=10.251.3.0/24 gateway=10.250.1.1
add dst-address=10.251.2.0/24 gateway=10.250.1.1
add dst-address=10.252.10.0/26 gateway=10.250.1.1
add dst-address=10.250.40.0/30 gateway=10.250.1.1
