import rpimcp4822 as mcp
import time

dev1 = mcp.RPiMCP4822(max_speed_khz=1000)
dev1.setup_output_latch()
print("writing A to .4mV but not latching...")
dev1.write(400, 0)
time.sleep(2)
print("now writing .9V to B but still not latching")
dev1.write(900,1)
time.sleep(2)
print("writing 1.1V, waiting 2s to latch...")
dev1.write(1100,0)
time.sleep(1)
print("...1s...")
time.sleep(1)
print("latching 1.1V, immediately writing .5V but not latching, waiting 4s...")
dev1.update_output()
dev1.write(500, 0) # write channel A lower, but won't show up yet
time.sleep(2)
print("...2s...")
time.sleep(2)
print("updating output to .5V, immediately writing 1200mV, then waiting 2s but never latching...")
dev1.update_output()
dev1.write(1200, 0) # write 400mV to channel A
time.sleep(1)
print("...1s...")
time.sleep(1)

dev1.shutdown()
print("complete")