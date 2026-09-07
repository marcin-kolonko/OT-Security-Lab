# Communication Matrix

> **Scope:** OT Security Lab communication flows.
>
> The matrix describes expected application/network communication between systems.
> Firewall enforcement is documented separately in `02-Firewall-Rule-Matrix.md`.
>
> **Policy model:** Explicitly permitted communication only. Unlisted communication should be considered unauthorized unless required for infrastructure services.

## 1. OT / Industrial Communication

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| OT-CELL01-PLC-01 | OT-CELL01 | OT-SRV-MQTT-01 | OT-SRV | TCP / 1883 | → | Publish PLC telemetry and process data via MQTT | ALLOWED |
| OT-CELL02-PLC-01 | OT-CELL02 | OT-SRV-MQTT-01 | OT-SRV | TCP / 1883 | → | Publish PLC telemetry and process data via MQTT | ALLOWED |
| OT-CELL03-PLC-01 | OT-CELL03 | OT-SRV-MQTT-01 | OT-SRV | TCP / 1883 | → | Publish PLC telemetry and process data via MQTT | ALLOWED |
| OT-SRV-MQTT-01 | OT-SRV | OT-CELL01-PLC-01 | OT-CELL01 | TCP / ephemeral | ← | Return traffic for established MQTT sessions | ALLOWED |
| OT-SRV-MQTT-01 | OT-SRV | OT-CELL02-PLC-01 | OT-CELL02 | TCP / ephemeral | ← | Return traffic for established MQTT sessions | ALLOWED |
| OT-SRV-MQTT-01 | OT-SRV | OT-CELL03-PLC-01 | OT-CELL03 | TCP / ephemeral | ← | Return traffic for established MQTT sessions | ALLOWED |

## 2. OT Monitoring / Node-RED

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| DMZ-SRV-NodeRed-01 | DMZ | OT-SRV-MQTT-01 | OT-SRV | TCP / 1883 | → | Subscribe to and/or publish OT MQTT data | ALLOWED |
| OT-SRV-MQTT-01 | OT-SRV | DMZ-SRV-NodeRed-01 | DMZ | TCP / ephemeral | ← | Return traffic for established MQTT sessions | ALLOWED |
| OT-CELL01-PLC-01 | OT-CELL01 | DMZ-SRV-NodeRed-01 | DMZ | — | → | Direct PLC-to-Node-RED communication | NOT ALLOWED |
| OT-CELL02-PLC-01 | OT-CELL02 | DMZ-SRV-NodeRed-01 | DMZ | — | → | Direct PLC-to-Node-RED communication | NOT ALLOWED |
| OT-CELL03-PLC-01 | OT-CELL03 | DMZ-SRV-NodeRed-01 | DMZ | — | → | Direct PLC-to-Node-RED communication | NOT ALLOWED |

### MQTT Topics Used by Node-RED

| MQTT Topic | Source | Data | Consumer |
|---|---|---|---|
| `cell01/plc01/motor/speed` | OT-CELL01-PLC-01 | Motor speed / RPM | Node-RED |
| `cell01/plc01/motor/current` | OT-CELL01-PLC-01 | Motor current | Node-RED |
| `cell01/plc01/motor/temperature` | OT-CELL01-PLC-01 | Motor temperature | Node-RED |
| `cell01/plc01/belt/speed` | OT-CELL01-PLC-01 | Conveyor belt speed | Node-RED |
| `cell01/plc01/sensor/product` | OT-CELL01-PLC-01 | Product sensor data | Node-RED |
| `cell01/plc01/state` | OT-CELL01-PLC-01 | PLC / conveyor state | Node-RED |
| `cell02/plc01/motor/speed` | OT-CELL02-PLC-01 | Motor speed / RPM | Node-RED |
| `cell02/plc01/motor/current` | OT-CELL02-PLC-01 | Motor current | Node-RED |
| `cell02/plc01/motor/temperature` | OT-CELL02-PLC-01 | Motor temperature | Node-RED |
| `cell02/plc01/belt/speed` | OT-CELL02-PLC-01 | Conveyor belt speed | Node-RED |
| `cell02/plc01/sensor/product` | OT-CELL02-PLC-01 | Product sensor data | Node-RED |
| `cell02/plc01/state` | OT-CELL02-PLC-01 | PLC / conveyor state | Node-RED |
| `cell03/plc01/motor/speed` | OT-CELL03-PLC-01 | Motor speed / RPM | Node-RED |
| `cell03/plc01/motor/current` | OT-CELL03-PLC-01 | Motor current | Node-RED |
| `cell03/plc01/motor/temperature` | OT-CELL03-PLC-01 | Motor temperature | Node-RED |
| `cell03/plc01/belt/speed` | OT-CELL03-PLC-01 | Conveyor belt speed | Node-RED |
| `cell03/plc01/sensor/product` | OT-CELL03-PLC-01 | Product sensor data | Node-RED |
| `cell03/plc01/state` | OT-CELL03-PLC-01 | PLC / conveyor state | Node-RED |

## 3. Node-RED Dashboard

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| IT-PC-Host-01 | IT | DMZ-SRV-NodeRed-01 | DMZ | TCP / 1880 | → | Access to Node-RED web interface | ALLOWED |
| IT-PC-Host-01 | IT | DMZ-SRV-NodeRed-01 | DMZ | TCP / 9000 | → | Access to Portainer management interface | ALLOWED |

## 4. Secure Administration

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| IT-PC-Host-01 | IT | DMZ-SRV-JUMP | DMZ | TCP / 22 | → | SSH access to jump server | ALLOWED |
| IT-PC-Host-01 | IT | DMZ-SRV-JUMP | DMZ | UDP / 51820 | → | WireGuard VPN tunnel to jump server | ALLOWED |
| DMZ-SRV-JUMP | DMZ | OT-ENG-01 | OT-SRV | TCP / 22 | → | Secure SSH administration | ALLOWED |
| DMZ-SRV-JUMP | DMZ | OT-ENG-01 | OT-SRV | TCP / 3389 | → | Secure RDP administration | ALLOWED |
| OT-ENG-01 | OT-SRV | DMZ-SRV-JUMP | DMZ | TCP / ephemeral | ← | Return traffic for established administrative sessions | ALLOWED |

## 5. Infrastructure / Time Synchronization

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| DMZ-SRV-NTP | DMZ | IT-PC-Host-01 | IT | UDP / 123 | → | Time synchronization | ALLOWED |
| DMZ-SRV-NTP | DMZ | DMZ-FW-EDGE-01 | DMZ / FW | UDP / 53 | → | DNS resolution for external time synchronization | ALLOWED |

## 6. Firewall Management

| Source | Source Zone | Destination | Destination Zone | Protocol / Port | Direction | Purpose | Status |
|---|---|---|---|---|---|---|---|
| IT-PC-Host-01 | IT | DMZ-FW-EDGE-01 | Firewall | TCP / 443 | → | OPNsense web administration | ALLOWED |

## 7. Prohibited / Unused Communication

| Source | Destination | Protocol / Port | Expected Result | Reason |
|---|---|---|---|---|
| OT-CELL01-PLC-01 | OT-CELL02-PLC-01 | Any | BLOCK | Cell-to-cell communication not required |
| OT-CELL01-PLC-01 | OT-CELL03-PLC-01 | Any | BLOCK | Cell-to-cell communication not required |
| OT-CELL02-PLC-01 | OT-CELL03-PLC-01 | Any | BLOCK | Cell-to-cell communication not required |
| OT-CELL03-PLC-01 | OT-CELL01-PLC-01 | Any | BLOCK | Cell-to-cell communication not required |
| OT-CELL03-PLC-01 | OT-CELL02-PLC-01 | Any | BLOCK | Cell-to-cell communication not required |
| OT-CELL01-PLC-01 | DMZ network | Any | BLOCK | Direct OT-to-DMZ communication not required |
| OT-CELL02-PLC-01 | DMZ network | Any | BLOCK | Direct OT-to-DMZ communication not required |
| OT-CELL03-PLC-01 | DMZ network | Any | BLOCK | Direct OT-to-DMZ communication not required |
| DMZ hosts | OT-CELL01/02/03 | Any except explicitly permitted flows | BLOCK | OT network isolation |
| IT hosts | OT network | Any except explicitly permitted flows | BLOCK | IT-to-OT isolation |
| Any | Any | Any not explicitly listed | BLOCK | Default-deny security model |

## 8. Communication Flow Summary

| Flow ID | Source | Destination | Main Protocol | Security Purpose |
|---|---|---|---|---|
| COMM-01 | CELL01 PLC | OT MQTT | MQTT / TCP 1883 | Industrial telemetry |
| COMM-02 | CELL02 PLC | OT MQTT | MQTT / TCP 1883 | Industrial telemetry |
| COMM-03 | CELL03 PLC | OT MQTT | MQTT / TCP 1883 | Industrial telemetry |
| COMM-04 | Node-RED | OT MQTT | MQTT / TCP 1883 | OT monitoring |
| COMM-05 | IT workstation | Node-RED | HTTP / TCP 1880 | Monitoring dashboard |
| COMM-06 | IT workstation | Jump Server | SSH / TCP 22 | Secure administration |
| COMM-07 | IT workstation | Jump Server | WireGuard / UDP 51820 | Secure remote access |
| COMM-08 | Jump Server | OT Engineering Server | SSH / TCP 22 | OT administration |
| COMM-09 | Jump Server | OT Engineering Server | RDP / TCP 3389 | OT administration |
| COMM-10 | NTP Server | IT workstation | NTP / UDP 123 | Time synchronization |
| COMM-11 | NTP Server | Firewall | DNS / UDP 53 | External time resolution |
| COMM-12 | IT workstation | DMZ Firewall | HTTPS / TCP 443 | Firewall administration |

> **Note:** Node-RED flows are used for visualization and monitoring. The Node-RED dashboard does not provide direct control of PLCs or industrial equipment.