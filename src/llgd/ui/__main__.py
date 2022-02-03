"""UI Definition
"""
import sys
import logging
import PySimpleGUI as sg  # pylint: disable=import-error
from psgtray import SystemTray
from llgd.lib.llgd_lib import light_on, light_off, set_brightness, set_temperature


def main():
    """ Starts the UI
    """
    sg.theme('Default1')

    power_layout = [
        [sg.Radio('On', group_id="power", enable_events=True),
         sg.Radio('Off', group_id="power", enable_events=True)]]

    brightness_layout = [
        [sg.Slider(range=(1, 100), default_value=50,
                   resolution=1, orientation="horizontal", enable_events=True, )]]

    temperature_layout = [
        [sg.Slider(range=(2700, 6500), default_value=4600,
                   resolution=50, orientation="horizontal", enable_events=True, )]]

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

    trayMenu = ['', ['Show Window', 'Hide Window', '---',
                     'Power', ['On', 'Off'], 'Exit']]

    tray = SystemTray(trayMenu, single_click_events=False, window=window,
                      tooltip="Lumitra Glow", icon=sg.DEFAULT_BASE64_ICON)

    # The Event Loop
    while True:
        event, values = window.read()
        logging.debug(f"Event: [{event}] Values: {values}")
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
        elif event in (0, "On"):
            light_on()
        elif event in (1, "Off"):
            light_off()
        elif event == 2:
            set_brightness(int(values[event]))
        elif event == 3:
            set_temperature(int(values[event]))

    window.close()


def init():
    """
    Entrypoint into the UI
    """

    if __name__ == "__main__":
        sys.exit(main())


init()
