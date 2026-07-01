import streamlit as st
from ai_checker import check_pcb

st.set_page_config(page_title= "AI PCB Checker", page_icon=":electric_plug:")
st.title("AI PCB Checker", text_alignment = "center" )

netlist = st.file_uploader(label = "Upload your Altium netlist file:", type=["txt", "net"])

mcu = st.selectbox(label = "What MCU are you using:", options = ["ESP32", "STM32", "Arduino Uno", "Arduino Nano", "Raspberry Pi Pico", "Other"])
if mcu == "Other":
    mcu_custom = st.text_input("Please specify the MCU you are using:")
    if mcu_custom:
        mcu = mcu_custom

def check(mcu, netlist):
    st.info(f"Checking PCB design for {mcu}...")
    pcb = netlist.read().decode('utf-8')


if st.button("Submit", icon="✅"):
    if not netlist:
        st.error("Please upload a netlist file")
    elif not mcu:
        st.error("Please specify your MCU")
    else:
        check(mcu, netlist)
