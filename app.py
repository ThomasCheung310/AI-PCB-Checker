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


if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "database" not in st.session_state:
    st.session_state.database = {}
if "missing_parts" not in st.session_state:
    st.session_state.missing_parts = []
if "pcb_text" not in st.session_state:
    st.session_state.pcb_text = ""


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

if st.button("Submit", icon="✅"):
    if not netlist:
        st.error("Please upload a netlist file")
    elif not mcu:
        st.error("Please specify your MCU")
    else:
        pcb = netlist.read().decode('utf-8')
        st.session_state.pcb_text = pcb
        components = parse_components(pcb)
        database, missing = get_components(components)
        st.session_state.database = database
        st.session_state.missing_parts = missing
        st.session_state.stage = "missing_input" if missing else "ready"

if st.session_state.stage == "missing_input":        
    st.warning("Some parts were not found. Please provide specs if known (optional).")
    for i in st.session_state.missing_parts:
        st.write(f"**{i}**")
        voltage = st.text_input(f"Max voltage", key=f"v_{i}")
        current = st.text_input(f"Max current", key=f"c_{i}")
        st.session_state.database[i] = {
            "source": "user_input" if (voltage or current) else "unknown",
            "max_voltage": voltage if voltage else "unknown",
            "max_current": current if current else "unknown"
        }
    if st.button("Continue with Analysis"):
        st.session_state.stage = "ready"
        st.rerun()
        
if st.session_state.stage == "ready":  
    st.info(f"Checking PCB design for {mcu}...")
    database = json.dumps(st.session_state.database, indent=2)
    result = check_pcb(mcu, st.session_state.pcb_text, database)
    st.write(result)
    st.session_state.stage = "done"
    


