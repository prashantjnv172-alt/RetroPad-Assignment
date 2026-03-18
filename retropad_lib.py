from skidl import *

def make_mcu(ref):
    p = Part(tool=SKIDL, name='ATtiny814-SS', ref=ref, footprint='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm')
    p += [Pin(num=str(i)) for i in range(1, 15)]
    p['1'].name = 'VDD'
    p['14'].name = 'GND'
    return p

def make_2pin(name, ref, val='', fp=''):
    p = Part(tool=SKIDL, name=name, ref=ref, value=val, footprint=fp)
    p += [Pin(num='1'), Pin(num='2')]
    return p

def make_db9(ref):
    p = Part(tool=SKIDL, name='DB9_Male', ref=ref, footprint='Connector_Dsub:DSUB-9_Male_EdgeMount_P2.77mm')
    p += [Pin(num=str(i)) for i in range(1, 10)]
    return p

def make_header(ref):
    p = Part(tool=SKIDL, name='Conn_01x06_Female', ref=ref, footprint='Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal')
    p += [Pin(num=str(i)) for i in range(1, 7)]
    return p

def make_hole(ref):
    p = Part(tool=SKIDL, name='MountingHole_Pad', ref=ref, footprint='MountingHole:MountingHole_4mm_Pad_Via')
    p += Pin(num='1')
    return p