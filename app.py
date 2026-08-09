import streamlit as st
from ai_checker import check_pcb
from cache import get_components
import json

st.set_page_config(page_title= "AI PCB Checker", page_icon=":electric_plug:")
st.title("AI PCB Checker", text_alignment = "center" )

netlist = st.file_uploader(label = "Upload your Altium netlist file:", type=["txt", "net"])

mcu = st.selectbox(label = "What MCU are you using:", options = ["ESP32", "STM32", "Arduino Uno", "Arduino Nano", "Raspberry Pi Pico", "Other"])
if mcu == "Other":
    mcu_custom = st.text_input("Please specify the MCU you are using:")
    if mcu_custom:
        mcu = mcu_custom

def parse_components(pcb):
    components = []
    in_components = False
    for i in pcb.split("\n"):
        if "COMPONENTS" in i:
            in_components = True
            continue
        if in_components == True and i.strip():
            parts = i.strip().split()
            if len(parts) >= 2:
                components.append(parts[1])
    return components

def check(mcu, netlist):
    st.info(f"Checking PCB design for {mcu}...")
    pcb = netlist.read().decode('utf-8')
    components = parse_components(pcb)
    database, missing = get_components(components)
    database = json.dumps(database, indent=2)
    
    if missing:
        #add check for missing parts
    result = check_pcb(mcu, pcb, database)
    
    st.write(result)

if st.button("Submit", icon="✅"):
    if not netlist:
        st.error("Please upload a netlist file")
    elif not mcu:
        st.error("Please specify your MCU")
    else:
        check(mcu, netlist)
