import pydynamixel.packet as pk
import pydynamixel.connection
import pydynamixel.instruction_packet as ip
import time

c = connection.Connection()
c.send(ip.InstructionPacket(1, ip.WRITE_DATA, (pk.LED, 1)))
time.sleep(2)
c.send(ip.InstructionPacket(1, ip.WRITE_DATA, (pk.LED, 0)))
