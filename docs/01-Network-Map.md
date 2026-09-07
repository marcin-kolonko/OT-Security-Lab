# Network documentation of OT/ICS lab (IPAM)

## IT (Office)
| Hostname | IP Address | Gateway | Description / Function |
| :--- | :--- | :--- | :--- |
| `IT-PC-Host01` | `10.250.0.1/24` | `-` | Main Host PC Windows 11 Pro |

---

## DMZ (Buffer)
| Hostname | IP Address | Mask / CIDR | Gateway | Description / Function |
| :--- | :--- | :--- | :--- | :--- |
| `DMZ-SRV-NodeRed01` | `10.250.50.10` | `/24` | `10.250.50.1` | Server Node-RED |
| `DMZ-SRV-NTP` | `10.250.50.25` | `/24` | `10.250.50.1` | Server NTP |
| `DMZ-SRV-JUMP` | `10.250.50.20` | `/24` | `10.250.50.1` | Jump Server / Bastion |
---


## OT Zone (ICS)
| Hostname | IP Address | Mask / CIDR |  Gateway | Description / Function |
| :--- | :--- | :--- | :--- | :--- |
| `OT-SRV-MQTT-01` | `10.252.10.11` | `/26` | `10.252.10.1` | MQTT Broker (Ubuntu Linux) |
| `OT-ENG-01` | `10.252.0.10` | `/26` | `10.252.0.1` | Simulation of Engineering station (Lubuntu 24.10) |
| `OT-CELL01-PLC-01` | `10.251.1.11` | `/26` | `10.251.1.1` | PLC production nest 01 |
| `OT-CELL01-HMI-01` | `10.251.1.12` | `/26` | `10.251.1.1` | HMI production nest 01 |
| `OT-CELL01-IR-01` | `10.251.1.13` | `/26` | `10.251.1.1` | Industrial Robot production nest 01 |
| `OT-CELL02-PLC-01` | `10.251.2.6` | `/24` | `10.251.2.1` | PLC production nest 02 |
| `OT-CELL02-HMI-01` | `10.251.2.10` | `/24` | `10.251.2.1` | HMI production nest 02 |
| `OT-CELL03-PLC-01` | `10.251.3.10` | `/24` | `10.251.3.1` | PLC production nest 03 |
| `OT-CELL03-HMI-01` | `10.251.3.20` | `/24` | `10.251.3.1` | HMI production nest 03 |

---


### `DMZ-FW-EDGE-01` OPNsense 26.1
| Interface / Port | Zone / Name | IP address | Mask / CIDR | Description / Function |
| :--- | :--- | :--- | :--- |:--- |
| `vtnet0` (WAN) | IT | `10.250.0.5`  | `/24` | Connection to IT and Internet |
| `vtnet1` (LAN) | OT / Industry | `10.250.40.2` | `/30` | Gateway to Industrial Network / OT |
| `vtnet2` (OPT1) | DMZ / Buffer zone | `10.250.50.1` | `/24` | Gateway to DMZ servers (Node-RED, Jump Server) |
| `vtnet3` (OPT2) | - | `-` | `-` | - |

---

### `OT-RTR-CORE-01` MikroTik CHR 7.22.1
| Interface / Subinterface | VLAN ID | Network name | IP address (Gateway) | Mask / CIDR | Description / Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ether1` | - | - | `-` | `-` | Reserve |
| `ether2` | - | DMZ | `10.250.40.1` | `30` | Transit to DMZ-FW-EDGE-01 |
| `ether3` | - | - | `-` | `-` | Reserve |
| `ether4` | - | OT-CELL01 | `10.250.1.1` | `30` | Transit to OT-CELL01 |
| `ether5` | - | OT-SW-ACC | `10.250.30.5` | `28` | Empty network  |
| `ether6` | - | - | `-` | `-` | Reserve |
| `ether7.102` | **VLAN 102** | OT-CELL02 | `10.251.2.1` | `/24` | Gateway for OT Cell02 |
| `ether7.103` | **VLAN 103** | OT-CELL03 | `10.251.3.1` | `/24` | Gateway for OT Cell03 |
| `ether7.200` | **VLAN 200** | OT-ENG-01 | `10.252.0.1` | `/26` | Gateway for Engineering station |
| `ether7.210` | **VLAN 210** | OT-SRV-MQTT-01 | `10.252.10.1` | `/26` | Gateway for MQTT broker |
| `ether8` | - | - | `-` | `-` | Reserve |

---

### `OT-RTR-DIST-01` MikroTik CHR 7.22.1
| Interface / Subinterface | VLAN ID | Network name | IP address (Gateway) | Mask / CIDR | Description / Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ether1` | - | OT-CORE | `10.250.1.2` | `/30` | Transit from OT-CORE-01 to OT-CELL01 |
| `ether2` | - | OT-CELL01 | `10.251.1.1` | `/26` | Gateway for OT-CELL01 |
| `ether3` ... `ether8` | - | - | `-` | `-` | Reserve |

---