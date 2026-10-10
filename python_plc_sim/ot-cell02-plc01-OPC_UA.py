import time
import random
import threading
import asyncio
from asyncua import Server, ua

# Globalne referencje do węzłów OPC UA i pętli zdarzeń
nodes = {}
loop = None

async def init_opcua_server():
    """Inicjalizacja i uruchomienie serwera OPC UA."""
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("PLC Simulation Server")

    # Rejestracja przestrzeni nazw i węzłów
    uri = "http://example.org/opcua/plc"
    idx = await server.register_namespace(uri)
    objects = server.get_objects_node()
    plc_folder = await objects.add_folder(idx, "PLC01")

    # Używamy AWAIT zamiast loop.run_until_complete!
    nodes['motor_speed'] = await plc_folder.add_variable(ua.NodeId("MotorSpeed", idx), "MotorSpeed", 0, ua.VariantType.Int32)
    nodes['current'] = await plc_folder.add_variable(ua.NodeId("Current", idx), "Current", 0.0, ua.VariantType.Float)
    nodes['temperature'] = await plc_folder.add_variable(ua.NodeId("Temperature", idx), "Temperature", 36.4, ua.VariantType.Float)
    nodes['belt_speed'] = await plc_folder.add_variable(ua.NodeId("BeltSpeed", idx), "BeltSpeed", 0.0, ua.VariantType.Float)
    nodes['product_detected'] = await plc_folder.add_variable(ua.NodeId("ProductDetected", idx), "ProductDetected", 0, ua.VariantType.Int32)
    nodes['state'] = await plc_folder.add_variable(ua.NodeId("State", idx), "State", "WAITING", ua.VariantType.String)

    # Ustawienie uprawnień do zapisu dla wszystkich zmiennych
    for node in nodes.values():
        await node.set_writable()

    print("Serwer OPC UA wystartował pod: opc.tcp://localhost:4840/freeopcua/server/")
    
    async with server:
        while True:
            await asyncio.sleep(1)

def start_opcua_thread():
    """Funkcja do uruchomienia pętli zdarzeń asyncio w osobnym wątku."""
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_opcua_server())

def set_opc_value(node_key, val, variant_type):
    """Zwykła funkcja wywoływana z pętli głównej (bez await)."""
    if loop and loop.is_running() and node_key in nodes:
        # Przekazanie operacji zapisu do pętli zdarzeń serwera
        var = ua.Variant(val, variant_type)
        coro = nodes[node_key].write_value(var)
        asyncio.run_coroutine_threadsafe(coro, loop)


# 1. Uruchomienie serwera OPC UA w tle
server_thread = threading.Thread(target=start_opcua_thread, daemon=True)
server_thread.start()

# Odczekanie chwili na inicjalizację serwera
time.sleep(2)


state = "WAITING"
state_start = time.time()
motor_speed = 0
current = 0.2
temperature = 36.4
belt_speed =  0
product_detected = 0
state_stop = 0

try:
    while True:

        now = time.time()

        if state == "WAITING":
            motor_speed = 0
            current = 0.2
            temperature = 36.4
            belt_speed =  0

        if state == "WAITING" and now - state_start > (2 + random.uniform(0, 6)):
            state = "RUNNING"
            product_detected = 1

        if state == "RUNNING" and motor_speed < 1500:
            motor_speed = motor_speed + random.randint(150, 200)
            current = round(motor_speed / 700, 2)
            temperature = round(temperature + random.uniform(0, 0.3), 2)
            belt_speed = round(motor_speed / 800, 2)


        if state == "RUNNING" and motor_speed >= 1500:

            state = "STOPPING"
            product_detected = 0

        if state == "STOPPING":
            motor_speed = motor_speed - random.randint(200, 400)
            if motor_speed < 0:
                motor_speed = 0
                state = "WAITING"
                state_start = time.time()
            current = round(motor_speed / 700, 2)
            temperature = round(temperature - random.uniform(0, 0.3), 2)
            if temperature < 36.4:
                temperature = 36.4
            belt_speed = round(motor_speed / 800, 2)

        set_opc_value('motor_speed', int(motor_speed), ua.VariantType.Int32)
        set_opc_value('current', float(current), ua.VariantType.Float)
        set_opc_value('temperature', float(temperature), ua.VariantType.Float)
        set_opc_value('belt_speed', float(belt_speed), ua.VariantType.Float)
        set_opc_value('product_detected', int(product_detected), ua.VariantType.Int32)
        set_opc_value('state', str(state), ua.VariantType.String)

        print(f"Stan: {state}, Prędkość silnika: {motor_speed}, Prąd: {current}, Temperatura: {temperature}, Prędkość taśmy: {belt_speed}, Produkt wykryty: {product_detected}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nZatrzymywanie programu...")
