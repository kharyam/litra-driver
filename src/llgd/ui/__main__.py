"""UI Definition
"""
import logging
import sys
import PySimpleGUI as sg  # pylint: disable=import-error
from psgtray import SystemTray  # pylint: disable=import-error
from llgd.lib.llgd_lib import light_on, light_off, set_brightness, set_temperature
from llgd.config.llgd_config import LlgdConfig


def main():

    config = LlgdConfig()
    initial_settings = config.read_current_state()
    default_brightness = 50 if initial_settings[LlgdConfig.BRIGHT] == None else initial_settings[LlgdConfig.BRIGHT]
    default_temp = 4600 if initial_settings[LlgdConfig.TEMP] == None else initial_settings[LlgdConfig.TEMP]

    """ Starts the UI
    """
    sg.theme('Default1')

    power_layout = [
        [sg.Radio('On', group_id="power", enable_events=True, key='on'),
         sg.Radio('Off', group_id="power", enable_events=True, key='off')]]

    brightness_layout = [
        [sg.Slider(range=(1, 100),
                   default_value=default_brightness,
                   resolution=1, orientation="horizontal", enable_events=True, key='bright')]]

    temperature_layout = [
        [sg.Slider(range=(2700, 6500), default_value=default_temp,
                   resolution=50, orientation="horizontal", enable_events=True, key='temp')]]

    power_frame = [
        [sg.Frame('Power', layout=power_layout)]]

    brightness_frame = [
        [sg.Frame('Brightness', layout=brightness_layout)]]

    temperature_frame = [
        [sg.Frame('Temperature', layout=temperature_layout)]]

    main_layout = [power_frame, brightness_frame,
                   temperature_frame, [sg.Exit()]]
    window = sg.Window('Logitech Lumitra Glow',
                       main_layout, enable_close_attempted_event=True)

    tray_menu = ['', ['Show Window', 'Hide Window', '---',
                      'On', 'Off', 'Exit']]

    tray = SystemTray(tray_menu, single_click_events=False, window=window,
                      tooltip="Lumitra Glow", icon=sg.EMOJI_BASE64_HAPPY_IDEA)

    # The Event Loop
    while True:
        event, values = window.read()
        if event == tray.key:
            event = values[event]
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()
        elif event.lower() == 'on':
            light_on()
        elif event.lower() == 'off':
            light_off()
        elif event == "bright":
            set_brightness(int(values[event]))
        elif event == "temp":
            set_temperature(int(values[event]))

    window.close()


if __name__ == "__main__":
    sys.exit(main())
