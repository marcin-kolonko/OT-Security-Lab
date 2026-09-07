# Firewall Rule Matrix

> **Policy model:** Explicit allow / default deny
>
> Network firewalls use connection tracking where applicable.
> Return traffic for permitted sessions is explicitly allowed using
> `connection-state=established,related` on MikroTik routers.

## 1. OPNsense DMZ-FW-EDGE-01
| Interface | Source | Destination |  Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-----------------|-------| :--- | :--- |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-NodeRed-01 | TCP / 1880 | ALLOW | Access to Node-RED | [x] |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-NodeRed-01 | TCP / 9000 | ALLOW | Access to Portainer | [x] |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-JUMP | TCP / 22 (SSH) | ALLOW | Access to Jump server | [x] |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-NTP | TCP / 22 (SSH) | ALLOW | Access to NTP server | [x] |
| WAN (IT) | IT-PC-Host-01  | DMZ-SRV-JUMP | UDP / 51820 | ALLOW | Allowing VPN Tunneling access from a Windows 11 Pro to Jump server | [x] |
| WAN (IT) | IT-PC-Host-01  | DMZ-FW-EDGE-01 | TCP / 443 | ALLOW | Access to Firewall GUI | [x] |
| *WAN (IT) | Any  | Any | All        | BLOCK | *Default deny — all traffic not explicitly permitted above  | [x] |
| OPT1 (DMZ) | DMZ-SRV-JUMP | OT-ENG-01 | TCP / 22 (SSH) | ALLOW | SSH administrative access from DMZ-SRV-JUMP to OT-ENG-01 | [x] |
| OPT1 (DMZ) | DMZ-SRV-JUMP | OT-ENG-01 | TCP / 3389 (RDP) | ALLOW | RDP administrative access from DMZ-SRV-JUMP to OT-ENG-01 | [x] |
| OPT1 (DMZ) | DMZ-SRV-NTP | IT-PC-Host-01 | UDP / 123 (NTP) | ALLOW | NTP time server Communication | [x] |
| OPT1 (DMZ) | DMZ-SRV-NTP | DMZ-FW-EDGE-01 | UDP / 53 (DNS) | ALLOW | Allow resolve DNS fro communicating with external time server | [x] |
| OPT1 (DMZ) | DMZ-SRV-NodeRed-01  | OT-SRV-MQTT-01 | TCP / 1883 (MQTT) | ALLOW | Connection from DMZ-SRV-NodeRed-01 to MQTT broker | [x] |
| *OPT1 (DMZ) | Any  | Any | All | BLOCK | *Default deny — all traffic not explicitly permitted above  | [x] |
| *LAN (OT) | Any  | Any | All | BLOCK | *Default deny — all traffic not explicitly permitted above | [x] |


## 2. MikroTik CHR / Router Core OT-RTR-CORE-01
| Source (VLAN)      | Destination (VLAN)     | Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-------|------| :--- |
| OT-CELL01-PLC-01  | OT-SRV-MQTT-01 (210)  | TCP / 1883 (MQTT) | ALLOW | Communication from PLC in CELL01 to MQTT broker | [x] |
| OT-CELL02-PLC-01 (102) | OT-SRV-MQTT-01 (210)  | TCP / 1883 (MQTT) | ALLOW | Communication from PLC in CELL02 to MQTT broker | [x] |
| OT-CELL03-PLC-01 (103) | OT-SRV-MQTT-01 (210) | TCP / 1883 (MQTT) | ALLOW | Communication from PLC in CELL03 to MQTT broker | [x] |
| DMZ-SRV-JUMP  | OT-ENG-01 (200) | TCP / 22 (SSH) | ALLOW |Secure administrative access to OT-ENG-01 from Jump Server or VPN tunneling | [x] |
| DMZ-SRV-JUMP  | OT-ENG-01 (200) | TCP / 3389 (RDP) | ALLOW |Secure administrative access through RDP to OT-ENG-01 from Jump Server or VPN tunneling | [x] |
| DMZ-SRV-NodeRed-01  | OT-SRV-MQTT-01 | TCP / 1883 (MQTT) | ALLOW | Connection from Node-RED to MQTT broker in the OT network | [x] |
| OT-SRV-MQTT-01 (210) | OT-CELL01-PLC-01 | TCP / Any | ALLOW | Established/related return traffic for MQTT sessions initiated by OT-CELL01-PLC-01 | [x] |
| OT-SRV-MQTT-01 (210) | OT-CELL02-PLC-01 (102) | TCP / Any | ALLOW | Established/related return traffic for MQTT sessions initiated by OT-CELL01-PLC-02  | [x] |
| OT-SRV-MQTT-01 (210) | OT-CELL03-PLC-01 (103) | TCP / Any | ALLOW | Established/related return traffic for MQTT sessions initiated by OT-CELL01-PLC-03  | [x] |
| OT-SRV-MQTT-01 (210) | DMZ-SRV-NodeRed-01 | TCP / Any | ALLOW | Established/related return traffic for MQTT sessions initiated by Node-RED  | [x] |
| OT-ENG-01 (200) | DMZ-SRV-JUMP | TCP | ALLOW | Established/related return traffic for SSH sessions initiated by Jump server  | [x] |
| Any  | Any | All | BLOCK | Default deny — all traffic not explicitly permitted above  | [x] |


## 3. MikroTik CHR / Router Distribution OT-RTR-DIST-01 
| Source (VLAN)      | Destination (VLAN)     | Protocol / Port | Action | Description | Implemented |
|--------------------|----------------|-----------------|-------|------| :--- |
| OT-CELL01-PLC-01  | OT-SRV-MQTT-01 (210)  | TCP / 1883 (MQTT) | ALLOW | Communication from PLC in CELL01 to MQTT broker | [x] |
| OT-SRV-MQTT-01 (210) | OT-CELL01-PLC-01 | TCP / Any | ALLOW | EEstablished/related return traffic for MQTT sessions initiated by OT-CELL01-PLC-01  | [x] |
| Any  | Any | All | BLOCK | Default deny — all traffic not explicitly permitted above  | [x] |

