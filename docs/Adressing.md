ADRESACJA LABORATORIUM
======================

1. SEGMENTY / PODSIECI
----------------------

LAB-MGMT
Network:	10.250.0.0/24
Gateway:	10.250.0.5

AUX/EDGE
Network:	10.250.30.0/28
Gateway:	10.250.30.5

INTERNET
Network:	NAT DHCP
Gateway:	NAT DHCP

TRANSIT
10.250.1.0/30       CELL01
10.250.2.0/30       CELL0x
10.250.3.0/30       CELL0x
...

CELL CONTROL
10.251.1.0/26       CELL01
10.251.2.0/26       CELL0x
10.251.3.0/26       CELL0x

CELL ZONES
192.168.60.0/24     CELL03
192.168.70.0/24     CELL02

2. MKT-1
---------

ether1 (LAB-MGMT): 	10.250.0.5/24
ether2 (CELL03)		192.168.60.1/24
ether3 (CELL02)		192.168.70.1/24
ether4 (CELL01)		10.250.1.1/30
ether5 (AUX/EDGE)	10.250.30.5/28
ether6			-
ether7			-
ether8			-

ROUTING:

10.250.0.0/24      connected
192.168.60.0/24    connected
192.168.70.0/24    connected
10.250.1.0/30      connected
10.250.30.0/28     connected

10.251.1.0/26      → 10.250.1.2

3. MKT-2:
----------

ether1 (TRANSIT-CELL01)	10.250.1.2/30
ether2 (CELL01)		10.251.1.1/26
ether3			-
ether4			-
ether5			-
ether6			-
ether7			-
ether8			-


ROUTING:

10.250.1.0/30      connected
10.251.1.0/26      connected

192.168.60.0/24    → 10.250.1.1
192.168.70.0/24    → 10.250.1.1

4. CELL01 'SQUIRTLE' 
----------

Network:		10.251.1.0/26
Gateway:		10.251.1.1

CELL01-PLC01:		10.251.1.11/26		(Alpine Linux 3.18.4 + Python + MQTT)
CELL01-HMI01:		10.251.1.12/26		(VPCS)
CELL01-ROB01:		10.251.1.13/26		(VPCS)

5. CELL02 'PIKACHU'
------------

Network:		192.168.70.0/24
Gateway:		192.168.70.1

CELL02-PLC01		192.168.70.6/24		(Alpine Linux 3.18.4 + Python + MQTT)
CELL02-HMI01		192.168.70.10/24	(VPCS)
OT-MQTT			192.168.70.11/24	(Ubuntu 24.04.1 LTS)

6. CELL03 'CHARMANDER'
------------
Network:		192.168.60.0/24
Gateway:		192.168.60.1

CELL03-PLC01		192.168.60.10/24	(Alpine Linux 3.18.4 + Python + MQTT)
CELL03-HMI01		192.168.60.20/24	(VPCS)

7. UBUNTU EDGE
--------------

Ubuntu 26.04 LTS

eth0	Internet / NAT
	DHCP
	192.168.137.x

eth1	LAB-MGMT
	10.250.0.10/24

eth2	AUX/EDGE
	10.250.30.10/28

8. GNS3
-------

GNS3 2.2.26
eth0	LAB-MGMT
	10.250.0.20/24
eth1	AUX/EDGE
	10.250.30.1/28

9. Windows 11 PRO

LabSwitch
10.250.0.1/24

NATSwitch
192.168.137.1/24

Ethernet / LAN
192.168.50.2/24

10. ROUTING - ACTUAL STATE

OT_Zone_1
192.168.70.0/24
        │
        ▼
MKT-1
        │
        ├── 10.250.1.1
        ▼
MKT-2
10.250.1.2
        │
        ▼
CELL-01
10.251.1.0/26


OT_Zone_2
192.168.60.0/24
        │
        ▼
MKT-1
        │
        ▼
MKT-2
        │
        ▼
CELL-01


AUX/EDGE
10.250.30.0/28
        │
        ▼
MKT-1

11. Networking tests
--------------------

CELL01 → MKT-1			OK
CELL01 → AUX/EDGE		OK

CELL03 → MKT-1			OK
CELL03 → CELL01			OK
CELL03 → AUX/EDGE		OK
CELL03 → LAB-MGMT		BLOCKED

CELL03 → MKT-1			OK
CELL03 → CELL01			OK
CELL03 → AUX/EDGE		OK

Ubuntu → MKT-1			OK
Ubuntu → CELL01			OK