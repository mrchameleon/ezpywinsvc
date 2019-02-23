## ezpywinsvc - An easy to use python windows service starter kit

ezpywinsvc is a starter kit for building robust windows service(s) in python!

There are some basic logging, failure handling, and packages for interacting with APIs/Databases bundled in.

I created this because I had a need to query a database on a regular basis and sync data from app to another via REST API. I needed as close to 24/7 stability as possible, and windows services are great for ensuring that the script will remain running at all times.

The advantage of this solution of making a python script into a service over others is it has broad compatibility with most modern versions of Windows and there is no Windows Service-specific python control code needed. The python script is converted to a portable .exe file that doesn't require python to be installed on the system to run. NSSM (The non-sucking service manager) (https://nssm.cc) is the tool I use to build the service from the compiled exe, and is much easier to create services with than the official Microsoft tools.

Obviously the focus here is windows-only, but with a little extra work, this can also run on linux as a daemonized process. 

Let me know if you end up using or liking this, or have any questions/trouble! rjs6143@gmail.com

### Setup Notes

Ensure python & pip are installed and available on PATH. I tested with python 3.6, but I have also used this with 2.7 many times. It was originally written in 2.7, but when I open-sourced the generic version I used 3.6.

When I build services, I use 32-bit python only. This is to ensure compatibility with certain db libraries (pyodbc), pyinstaller, and other dependecies. 

If using pyodbc, also make sure your created ODBC datasource a 32-bit datasource as well. (C:\windows\syswow64\odbcad32.exe on 64-bit systems)


### Quick Setup

1. git clone or download/extract the repo; open command prompt as administrator

2. `virtualenv -p python ezpywinsvc`

3. `reqs.bat` (includes additional manual pip install command for pyinstaller. The develop branch of pyinstaller is used because it has a bugfix that the so-called stable version doesn't have which will break app compilation with certain python packages. Kinda backwards, isn't it?)

4. `build.bat` to build an exe of the app, based on service.spec (will need customization if you rename the service's directory/exe name/icon, etc). Whitelist the entire directory with antivirus first so it doesn't get blacklisted with active monitoring. 

5. If the app compiled to an exe successfully ( good luck :) ), you are ready to turn it into a service! Follow the service setup instructions below.



### Service setup process

1. before building/rebuilding as an EXE with `build.bat`, ALWAYS ensure DEBUG=False, and SERVICE_MODE=True in service.py (they are by default)

2. Download nssm (non-sucking service manager) from https://nssm.cc/, Extract the zip, copy the 32bit nssm.exe into the main directory.

3. Open command prompt as administrator

4. `cd c:\ezpywinsvc`

5. `nssm.exe install myservice`   (Remember what you typed here for removal purposes, but it is the "name" of the service - You can look it up in services.msc if you forget)

6. Choose the exe from the dist path on the Application tab; Details tab to set service display name and description. 

7. Click "Install Service"

8. Test the service with services.msc (Windows Services) - debug.log will be created in the dist/myservice dir, and should be written to every 60 seconds.  Use a "tailing" log viewer such as BareTail (https://www.baremetalsoft.com/baretail/), or you will have to close/reopen the log file to see changes in notepad/most text editors.


### To remove the service if something isn't right:

`nssm.exe remove myservice`


### Dev/Test Cycle

There are two important flags in service.py: DEBUG and SERVICE_MODE.

If you are developing/testing the script in command prompt, set `DEBUG=True; SERVICE_MODE=False` in service.py. You can then run it like a normal python script `python service.py` and see what is normally only debug.log output printed to the window.

Before using `build.bat` to compile and run as a service, set `DEBUG=False; SERVICE_MODE=True` in service.py

Not doing so will crash your service, because `DEBUG=True` writes to the console window, which doesn't exist in a windowless python script.

SERVICE_MODE is a separate flag, because it sets how the script is running. SERVICE_MODE=False isn't strictly necessary to switch everytime. This is for supporting linux use/running as a script in DEBUG mode, and so that the auto-restart mechanisms to work correctly in the respective modes. When SERVICE_MODE=True,  (running as a windows service) `restart_application` kills the process which windows service manager will then restart automatically.  if `SERVICE_MODE=False`, it restarts the script using `python service.py`

If you only change minor things, and are confident its not going to need to be tested in debug mode, you can always leave the flags set for "production" mode (aka running it as a service, as above). STOP the running service if it is running. Then just run `build.bat` to recompile. Start the service again. Verify correct output in dist/myservice/debug.log

### Some recommended bundled libraries to help build your service

pyodbc - database connectivity
schedule - schedule subprocesses to run on regular basis
simplejson - json parsing
requests - make http requests
rollbar - error reporting
datadog - timeseries data graphs/monitoring