from skidl import *
from retropad_lib import * # -----------------------------------------------------------------------------
# 1. Initialize Components
# -----------------------------------------------------------------------------

mcu = make_mcu('U1')

j1_db9  = make_db9('J1')
j2_updi = make_header('J2')

sw_fp = 'RetroPad:Silicone_Membrane_Pad_11mm_(7.5mm)'
sw_jump  = make_2pin('SW_Push', 'JUMP1', fp=sw_fp)
sw_up    = make_2pin('SW_Push', 'UP1', fp=sw_fp)
sw_down  = make_2pin('SW_Push', 'DOWN1', fp=sw_fp)
sw_left  = make_2pin('SW_Push', 'LEFT1', fp=sw_fp)
sw_right = make_2pin('SW_Push', 'RIGHT1', fp=sw_fp)
sw_rapid = make_2pin('SW_Push', 'RAPID1', fp=sw_fp)
sw_btn1  = make_2pin('SW_Push', 'BTN1', fp=sw_fp)
sw_btn2  = make_2pin('SW_Push', 'BTN2', fp=sw_fp)
sw_btn3  = make_2pin('SW_Push', 'BTN3', fp=sw_fp)

res_fp = 'Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder'
r1  = make_2pin('R_US', 'R1', val='1K', fp=res_fp)  # POTX Divider Top
r2  = make_2pin('R_US', 'R2', val='1K', fp=res_fp)  # POTY Divider Top
r3  = make_2pin('R_US', 'R3', val='330', fp=res_fp) # LED Resistor
r4  = make_2pin('R_US', 'R4', val='1K', fp=res_fp)  # FIRE Pull-down
r5  = make_2pin('R_US', 'R5', val='1K', fp=res_fp)  # POTX Divider Bottom
r6  = make_2pin('R_US', 'R6', val='1K', fp=res_fp)  # POTY Divider Bottom

r7  = make_2pin('R_US', 'R7', val='0', fp=res_fp)
r8  = make_2pin('R_US', 'R8', val='0', fp=res_fp)
r9  = make_2pin('R_US', 'R9', val='0', fp=res_fp)
r10 = make_2pin('R_US', 'R10', val='0', fp=res_fp)
r11 = make_2pin('R_US', 'R11', val='0', fp=res_fp)

led = make_2pin('LED', 'D1', fp='LED_THT:LED_D3.0mm')
led['1'].name = 'K'
led['2'].name = 'A'

c1 = make_2pin('C_Small', 'C1', val='0.1uF', fp='Capacitor_SMD:CP_Elec_4x4.5')

h1 = make_hole('H1')
h2 = make_hole('H2')

# -----------------------------------------------------------------------------
# 2. Define Global Nets
# -----------------------------------------------------------------------------
vcc = Net('+5V')
gnd = Net('GND')

net_up    = Net('UP')
net_down  = Net('DOWN')
net_left  = Net('LEFT')
net_right = Net('RIGHT')
net_fire  = Net('FIRE')
net_potx  = Net('POTX')
net_poty  = Net('POTY')

net_btn1  = Net('BTN1')
net_btn2  = Net('BTN2')
net_btn3  = Net('BTN3')
net_rapid = Net('RAPID')

net_out_btn2 = Net('OUT_BTN2')
net_out_btn3 = Net('OUT_BTN3')
net_reset    = Net('RESET')

# -----------------------------------------------------------------------------
# 3. Connections
# -----------------------------------------------------------------------------

# Power & Ground Distribution
vcc += mcu['1'], c1['1'], j2_updi['2'], j1_db9['7']
gnd += mcu['14'], c1['2'], j2_updi['6'], j1_db9['8'], h1['1'], h2['1']

# Grounding all switches
gnd += sw_jump['1'], sw_up['1'], sw_down['1'], sw_left['1'], sw_right['1']
gnd += sw_rapid['1'], sw_btn1['1'], sw_btn2['1'], sw_btn3['1']

# Grounding the voltage dividers and pull-down
gnd += r4['2'], r5['2'], r6['2']

# --- HARDWARE PASSTHROUGH (D-PAD) ---
# D-Pad routes directly to DB9 via 0-ohm resistors
net_up    += r8['1'], j1_db9['1']
sw_up['2'] += r8['2']

net_down  += r9['1'], j1_db9['2']
sw_down['2'] += r9['2']

net_left  += r10['1'], j1_db9['3']
sw_left['2'] += r10['2']

net_right += r11['1'], j1_db9['4']
sw_right['2'] += r11['2']

# JUMP is hardwired to act as UP
sw_jump['2'] += r7['2']
net_up += r7['1']

# --- SMART CONTROLLER INPUTS ---
net_btn1  += sw_btn1['2'], mcu['2']
net_btn2  += sw_btn2['2'], mcu['3']
net_btn3  += sw_btn3['2'], mcu['4']
net_rapid += sw_rapid['2'], mcu['5']

# --- SMART CONTROLLER OUTPUTS ---
# FIRE Output (with R4 pull-down to GND)
net_fire += mcu['6'], r4['1'], j1_db9['6']

# Analog POT Simulation (Voltage Dividers)
net_out_btn3 += mcu['8'], r1['2']
net_potx     += r1['1'], r5['1'], j1_db9['5'] 

net_out_btn2 += mcu['7'], r2['2']
net_poty     += r2['1'], r6['1'], j1_db9['9']

# --- PERIPHERALS ---
# RAPID LED Indicator
net_rapid += r3['1']
r3['2'] += led['A']
gnd += led['K']

# UPDI Programming
net_reset += j2_updi['1'], mcu['10']

# -----------------------------------------------------------------------------
# 4. Generate Output
# -----------------------------------------------------------------------------
ERC()
generate_netlist(file_='RetroPad_skidl.net')
