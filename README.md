# RGB_OFF
Turns off RGB when monitor turns off using [OpenRGB](https://github.com/CalcProgrammer1/OpenRGB)/[python](https://www.python.org/downloads/)</br>
Listens for changes in the monitor's power state using Windows' power management notifications. Sets an OpenRGB profile when monitor on/off is detected. </br>
</br>
</br>
<b>HOW TO:</b> </br>
Download script, save as `<NAME>.py` </br>
Install `OpenRGB`, make sure it is started with `--server` flag </br>
Install `python` </br>
Install dependencies `pip install pywin32` </br>
Change relevant paths `see BEFORE RUNNING` </br>
Run at startup using a batch file or task scheduler. I use `pythonw` to run in the background </br> 
</br>
</br>
<b>BEFORE RUNNING:</b> </br>
Make your on/off profiles in OpenRGB and save them </br>
<b>line 55</b></br>
change `C:\path\to\OpenRGB.exe` to your install path `command = [r"C:\path\to\OpenRGB.exe", "--profile", f"{profile}.orp"]` </br>
<b>line 70</b></br>
change profile name `on` to your <b>RGB ON</b> profile `set_openrgb_profile("on")` </br>
<b>line 72</b></br>
change profile name `off` to your <b>RGB OFF</b> profile `set_openrgb_profile("off")` </br>

