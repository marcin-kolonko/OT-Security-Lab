import asyncio
import logging
import random

from pymodbus.server import StartAsyncTcpServer
from pymodbus.simulator import SimData, SimDevice, DataType


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

log = logging.getLogger(__name__)


# ============================================================
# MODBUS DATA
# ============================================================

# Holding Registers:
#
# 40001 -> motor_speed
# 40002 -> current * 100
# 40003 -> temperature * 10
# 40004 -> belt_speed * 100
# 40005 -> product_detected
# 40006 -> state
#
# Adres wewnętrzny Modbus = 0

holding_registers = SimData(
    address=0,
    datatype=DataType.REGISTERS,
    values=[0] * 100
)


device = SimDevice(
    0,
    simdata=(
        # Coils
                [
            SimData(
                address=0,
                datatype=DataType.BITS,
                values=[False] * 100
            )
        ],

        # Discrete Inputs
        [
            SimData(
                address=0,
                datatype=DataType.BITS,
                values=[False] * 100
            )
        ],

        # Holding Registers
        [
            holding_registers
        ],

        # Input Registers
        [
            SimData(
                address=0,
                datatype=DataType.REGISTERS,
                values=[0] * 100
            )
        ],
    )
)


# ============================================================
# SIMULATION
# ============================================================

async def simulation_loop(server):

    state = "WAITING"
    state_start = asyncio.get_running_loop().time()

    motor_speed = 0
    current = 0.2
    temperature = 36.4
    belt_speed = 0
    product_detected = 0

    state_map = {
        "WAITING": 0,
        "RUNNING": 1,
        "STOPPING": 2,
    }

    while True:

        now = asyncio.get_running_loop().time()

        # ----------------------------------------------------
        # WAITING
        # ----------------------------------------------------

        if state == "WAITING":

            motor_speed = 0
            current = 0.2
            temperature = 36.4
            belt_speed = 0

            if now - state_start > (2 + random.uniform(0, 6)):
                state = "RUNNING"
                product_detected = 1

        # ----------------------------------------------------
        # RUNNING
        # ----------------------------------------------------

        if state == "RUNNING" and motor_speed < 1500:

            motor_speed += random.randint(150, 200)

            current = round(motor_speed / 700, 2)

            temperature = round(
                temperature + random.uniform(0, 0.3),
                2
            )

            belt_speed = round(motor_speed / 800, 2)

        if state == "RUNNING" and motor_speed >= 1500:

            state = "STOPPING"
            product_detected = 0

        # ----------------------------------------------------
        # STOPPING
        # ----------------------------------------------------

        if state == "STOPPING":

            motor_speed -= random.randint(200, 400)

            if motor_speed < 0:

                motor_speed = 0

                state = "WAITING"

                state_start = now

            current = round(motor_speed / 700, 2)

            temperature = round(
                temperature - random.uniform(0, 0.3),
                2
            )

            if temperature < 36.4:
                temperature = 36.4

            belt_speed = round(motor_speed / 800, 2)

        # ----------------------------------------------------
        # MODBUS VALUES
        # ----------------------------------------------------

        values = [
            int(motor_speed),
            int(current * 100),
            int(temperature * 10),
            int(belt_speed * 100),
            int(product_detected),
            int(state_map[state]),
        ]

        # ----------------------------------------------------
        # UPDATE REAL SERVER DATASTORE
        # ----------------------------------------------------

        await server.context.async_setValues(
            0,      # device_id
            3,      # function code = Holding Registers
            0,      # address
            values
        )

        log.info(
            "SERVER: %s | state=%s",
            values,
            state
        )

        await asyncio.sleep(1)


# ============================================================
# SERVER
# ============================================================

async def main():

    log.info("Uruchamianie symulatora Modbus TCP...")

    # Tworzymy task symulacji po uruchomieniu serwera.
    #
    # StartAsyncTcpServer blokuje aż do zakończenia serwera,
    # więc potrzebujemy uruchomić go jako task.

    server_task = asyncio.create_task(
        StartAsyncTcpServer(
            context=device,
            address=("0.0.0.0", 502),
        )
    )

    # Dajemy serwerowi chwilę na utworzenie kontekstu.
    await asyncio.sleep(0.2)

    # Pobieramy właściwy obiekt serwera.
    #
    # StartAsyncTcpServer nie zwraca nam bezpośrednio serwera,
    # więc zamiast tego korzystamy z aktywnego serwera PyModbus.

    from pymodbus.server import ModbusBaseServer

    while ModbusBaseServer.active_server is None:
        await asyncio.sleep(0.01)

    server = ModbusBaseServer.active_server

    log.info("Serwer działa na 0.0.0.0:502")

    simulation_task = asyncio.create_task(
        simulation_loop(server)
    )

    try:
        await asyncio.gather(
            server_task,
            simulation_task
        )

    except asyncio.CancelledError:

        simulation_task.cancel()

        raise


if __name__ == "__main__":

    asyncio.run(main())
