# Firewall Rule Matrix

## 1. OPNsense DMZ-FW-EDGE-01
| Interface | Source | Destination |  Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-----------------|-------| :--- | :--- |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-NodeRed-01 | TCP / 1880        | ALLOW | Access to Node-Red | [] |
| WAN (IT) | IT-PC-Host-01  | Jump Server | TCP SSH / 22 | ALLOW | Access to Jump server | [] |
| WAN (IT) | IT-PC-Host-01  | DMZ-FW-EDGE-01 | TCP / 443 | ALLOW | Access to Firewall GUI | [] |
| WAN (IT) | Any  | Any | All        | BLOCK | Direct traffic from IT prohibited  | [] |
| OPT1 (DMZ) | Jump server  | OT-CELL01-PLC-01 | TCP SSH / 22 | ALLOW |Secure administrative access to OT | [] |
| OPT1 (DMZ) | Jump server  | OT-CELL02-PLC-01 | TCP SSH / 22 | ALLOW |Secure administrative access to OT | [] |
| OPT1 (DMZ) | Jump server  | OT-CELL03-PLC-01 | TCP SSH / 22 | ALLOW |Secure administrative access to OT | [] |
| OPT1 (DMZ) | Jump server  | OT-SRV-MQTT-01 | TCP SSH / 22 | ALLOW |Secure administrative access to OT | [] |
| OPT1 (DMZ) | DMZ-SRV-NodeRed-01  | OT-SRV-MQTT-01 | TCP MQTT / 1883 | ALLOW | Connection to MQTT beoker inside of OT network | [] |
| OPT1 (DMZ) | Any  | Any | All | BLOCK | Direct traffic from DMZ prohibited  | [] |
| LAN (OT) | Any  | Any | All | BLOCK | Direct traffic from OT prohibited | [] |


## 2. MikroTik CHR / Router Core OT-RTR-CORE-01
| Source (VLAN)      | Destination (VLAN)     | Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-------|------| :--- |
| OT-CELL01-PLC-01  | OT-SRV-MQTT-01  | MQTT / 1883 | ALLOW | Communication from PLC in CELL01 to MQTT broker | [x] |
| OT-CELL02-PLC-01  | OT-SRV-MQTT-01  | MQTT / 1883 | ALLOW | Communication from PLC in CELL02 to MQTT broker | [x] |
| OT-CELL03-PLC-01  | OT-SRV-MQTT-01  | MQTT / 1883 | ALLOW | Communication from PLC in CELL03 to MQTT broker | [x] |
| Jump server  | OT-CELL01-PLC-01 | TCP / SSH 22 | ALLOW |Secure administrative access to OT | [] |
| Jump server  | OT-CELL02-PLC-01 | TCP / SSH 22 | ALLOW |Secure administrative access to OT | [] |
| Jump server  | OT-CELL03-PLC-01 | TCP / SSH 22 | ALLOW |Secure administrative access to OT | [] |
| Jump server  | OT-SRV-MQTT-01 | TCP / SSH 22 | ALLOW |Secure administrative access to OT | [] |
| DMZ-SRV-NodeRed-01  | OT-SRV-MQTT-01 | TCP MQTT / 1883 | ALLOW | Connection to MQTT beoker inside of OT network | [x] |
| Any  | Any | All | BLOCK | Direct traffic between subnets prohibited  | [x] |


## 3. MikroTik CHR / Router Distribution OT-RTR-DIST-01 
| Source (VLAN)      | Destination (VLAN)     | Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-------|------| :--- |
| Jump server  | OT-CELL01-PLC-01 | TCP / SSH 22 | ALLOW |Secure administrative access to OT | [] |
| OT-CELL01-PLC-01  | OT-SRV-MQTT-01  | MQTT / 1883 | ALLOW | Communication from PLC in CELL01 to MQTT broker | [x] |
| Any  | Any | All | BLOCK | Direct traffic between subnets prohibited  | [x] |




