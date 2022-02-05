"""UI Definition
"""
import sys
import PySimpleGUI as sg  # pylint: disable=import-error
from psgtray import SystemTray  # pylint: disable=import-error
from llgd.lib.llgd_lib import light_on, light_off, set_brightness, set_temperature
from llgd.config.llgd_config import LlgdConfig


def main():  # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # # pylint: disable=too-many-statements
    """ Starts the UI
    """

    config = LlgdConfig()
    initial_settings = config.read_current_state()
    default_brightness = 50 if initial_settings[config.BRIGHT] is \
        None else initial_settings[config.BRIGHT]
    default_temp = 4600 if initial_settings[config.TEMP] is \
        None else initial_settings[config.TEMP]

    sg.theme('Default1')

    power_layout = [
        [sg.Radio('On', group_id="power", enable_events=True, key='on'),
         sg.Radio('Off', group_id="power", enable_events=True, key='off')]]

    brightness_layout = [
        [sg.Slider(range=(1, 100),
                   default_value=default_brightness,
                   resolution=1, orientation="horizontal", enable_events=True, expand_x=True,
                   key='bright')]]

    temperature_layout = [
        [sg.Slider(range=(2700, 6500), default_value=default_temp,
                   resolution=50, orientation="horizontal", enable_events=True, expand_x=True,
                   key='temp')]]

    profile_layout = [sg.Combo(config.get_profile_names(), key='profiles',
                               default_value=config.CURRENT_PROFILE_NAME, readonly=True,
                               enable_events=True, tooltip="The currently selected profile",
                               expand_x=True, size=(20, 1)), sg.Button(
        'Save as...', key='save', tooltip="Save the current settings as a new profile"),
        sg.Button('Delete', key='delete', disabled=True, tooltip="Delete the selected profile")]

    power_frame = [
        [sg.Frame('Power', layout=power_layout)]]

    brightness_frame = sg.Frame(
        'Brightness', layout=brightness_layout, expand_x=True)

    temperature_frame = sg.Frame(
        'Temperature', layout=temperature_layout, expand_x=True)

    settings_layout = [profile_layout, [
        brightness_frame], [temperature_frame]]

    settings_frame = [[sg.Frame('Settings', layout=settings_layout)]]

    main_layout = [power_frame, settings_frame, [
        sg.Exit()], [sg.StatusBar("Updating current settings.", expand_x=True,
                                  background_color="#FFFFFF", key="status_bar")]]
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
            if values["profiles"] is not config.CURRENT_PROFILE_NAME:
                config.add_or_update_profile(
                    values["profiles"], brightness=int(values[event]))
        elif event == "temp":
            set_temperature(int(values[event]))
            if values["profiles"] is not config.CURRENT_PROFILE_NAME:
                config.add_or_update_profile(
                    values["profiles"], temp=int(values[event]))
        elif event == "profiles":
            if values[event] == config.CURRENT_PROFILE_NAME:
                window["delete"].update(disabled=True)
                window["save"].update(disabled=False)
                window["status_bar"].update(value="Updating current settings.")
            else:
                window["delete"].update(disabled=False)
                window["save"].update(disabled=True)
                settings = config.read_profile(values[event])
                set_brightness(settings[config.BRIGHT])
                set_temperature(settings[config.TEMP])
                window["bright"].update(settings[config.BRIGHT])
                window["temp"].update(settings[config.TEMP])
                window["status_bar"].update(
                    value=f'Updating profile "{values[event]}"')
        elif event == "delete":
            do_delete = sg.popup_yes_no(
                f'Delete profile "{values["profiles"]}"?', title="Delete Profile",
                background_color="#FF8888")
            if do_delete == "Yes":
                config.delete_profile(values["profiles"])
                window["profiles"].update(
                    values=config.get_profile_names(), value=config.CURRENT_PROFILE_NAME)
                window["delete"].update(disabled=True)
                window["save"].update(disabled=False)
                window["status_bar"].update(value="Updating current settings.")
        elif event == "save":
            profile_name = sg.popup_get_text(
                title="Create Profile", message="Enter profile name")
            if profile_name not in (config.CURRENT_PROFILE_NAME, None):
                config.add_or_update_profile(
                    profile_name, temp=values["temp"], brightness=values["bright"])
                window["profiles"].update(
                    values=config.get_profile_names(), value=profile_name)
                window["delete"].update(disabled=False)
                window["save"].update(disabled=True)

    window.close()


if __name__ == "__main__":
    sys.exit(main())
