ADRESACJA LABORATORIUM
======================

1. SEGMENTY / PODSIECI
----------------------

LAB-MGMT
Network:    10.250.0.0/24
Gateway:    10.250.0.5

TRANSIT
10.250.1.0/30       CELL01 ↔ MKT-1/MKT-2
10.250.2.0/30       reserved
10.250.3.0/30       reserved
...

AUX/EDGE
Network:    10.250.30.0/28
Gateway:    10.250.30.5

CELL CONTROL
10.251.1.0/26       CELL01 / legacy
10.251.2.0/24       CELL02 / VLAN 102
10.251.3.0/24       CELL03 / VLAN 103

OT SERVICES
10.252.10.0/26      OT-MQTT / VLAN 210

INTERNET
NAT / DHCP


2. MKT-1
---------

ether1  LAB-MGMT       10.250.0.5/24
ether2  legacy CELL02  -
ether3  legacy CELL03  -
ether4  CELL01         10.250.1.1/30
ether5  AUX/EDGE       10.250.30.5/28
ether6  -
ether7  OT-AGG-SW01   TRUNK
ether8  -

VLAN:

VLAN 102   CELL02       10.251.2.1/24
VLAN 103   CELL03       10.251.3.1/24
VLAN 210   OT-MQTT      10.252.10.1/26

ROUTING:

10.251.1.0/26    → 10.250.1.2
10.251.2.0/24    connected
10.251.3.0/24    connected
10.252.10.0/26   connected


3. MKT-2
---------

ether1  TRANSIT-CELL01   10.250.1.2/30
ether2  CELL01            10.251.1.1/26

ROUTING:

10.251.1.0/26    connected


4. OT-AGG-SW01
--------------

Open vSwitch

eth0    trunk → MKT-1 ether7
eth1    -
eth2    access VLAN 102 → CELL02
eth3    access VLAN 103 → CELL03
eth4    -
eth5    -
eth6    access VLAN 210
eth7    -

Management IP: none


5. CELL01 — SQUIRTLE
--------------------

Network:    10.251.1.0/26
Gateway:    10.251.1.1

CELL01-PLC01    10.251.1.11/26
CELL01-HMI01    10.251.1.12/26
CELL01-ROB01    10.251.1.13/26

Status: LEGACY CELL


6. CELL02 — PIKACHU
-------------------

VLAN:       102
Network:    10.251.2.0/24
Gateway:    10.251.2.1

CELL02-PLC01    10.251.2.6/24
CELL02-HMI01    10.251.2.10/24


7. CELL03 — CHARMANDER
----------------------

VLAN:       103
Network:    10.251.3.0/24
Gateway:    10.251.3.1

CELL03-PLC01    10.251.3.10/24
CELL03-HMI01    10.251.3.20/24


8. OT-MQTT
----------

VLAN:       210
Network:    10.252.10.0/26
Gateway:    10.252.10.1

OT-MQTT:    10.252.10.11/26

Service:
MQTT / Mosquitto — TCP 1883


9. UBUNTU EDGE
--------------

Ubuntu

eth0    Internet / NAT       DHCP
eth1    LAB-MGMT             10.250.0.10/24
eth2    AUX/EDGE             10.250.30.10/28


10. GNS3
--------

GNS3 Server

eth0    LAB-MGMT             10.250.0.20/24
eth1    AUX/EDGE             10.250.30.1/28


11. WINDOWS 11 PRO
------------------

LabSwitch
10.250.0.1/24

NATSwitch
192.168.137.1/24

Ethernet / LAN
192.168.50.2/24


12. OPNSENSE
------------------

NIC1 → WAN → LAB-MGMT
NIC2 → LAN/OT → MKT-1 ether2
NIC3 → DMZ → 10.250.50.0/24
NIC4 → rezerwa

WAN       → 10.250.0.x/24
LAN/OT    → 10.250.40.2/30
DMZ       → 10.250.50.1/24