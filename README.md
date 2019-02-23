## ezpywinsv - An easy to use python windows service template

Template for building a robust windows service from python code.

My inspiration was a need to query a database on a regular basis and sync data from app to another via REST API. I needed as close to 24/7 stability as possible, and windows services are great for ensuring that the script will remain running at all times.

Take advantage of my trial and error and learning which led to what I feel is the best way to build a production-ready python based windows service.

The advantage of this solution over others is broad compatibility with most modern versions of Windows and no Windows Service related python code needed.

(https://stackoverflow.com/questions/32404/how-do-you-run-a-python-script-as-a-service-in-windows)

The focus is windows-only, but a small guide to daemonizing this service template on linux would be trivial to add.



### Setup Notes

Ensure python 2.7 & pip are installed and available on PATH.

When I build services, I use 32 bit python only. This is to ensure compatibility with certain db libraries (pyodbc), pyinstaller, and other dependecies. 

Protip if using pyodbc, also make sure your created ODBC datasource a 32-bit datasource only. (C:\windows\syswow64\odbcad32.exe on 64-bit systems)


### Setup

1. git clone or download/extract the repo; open a windows cmd prompt as administrator

2. `virtualenv -p python ezpywinsvc`

3. `reqs.bat` (includes additional manual pip install command for pyinstaller. The develop branch of pyinstaller is used because it has a bugfix that the so-called stable version doesn't have which will break app compilation with certain python packages. Kinda backwards, isn't it?)

4. `build.bat` to build an exe of the app, based on service.spec (will need customization if you rename the service's directory/exe name/icon, etc). I hope it builds for you without errors, so best of luck! Whitelist the entire directory with antivirus first so it doesn't get blacklisted with active monitoring. 

5. If the app compiled to an exe successfully, you are ready to make it a service! Follow the service setup instructions below.



### Service setup

1. Download nssm (non-sucking service manager) from https://nssm.cc/, Extract the zip, pull the 32bit nssm.exe into your directory.

2. Open cmd.exe as an administrator;   cd c:\ezpywinsvc

3. nssm.exe install myservice   (Remember what you typed here for removal purposes, but it is the "name" of the service - You can look it up in services.msc if you forget)

4. Choose the exe from the dist path on the Application tab; Details tab to set service display name and description. 

5. Click "Install Service"

6. Test the service with services.msc (Windows Services) - debug.log will be created in the dist/myservice dir, and should be written to every 60 seconds.  Use a tailing log viewer like baretail (https://www.baremetalsoft.com/baretail/), or you will have to close/reopen the log file to see changes in notepad/most text editors.


### To remove the service if something isn't right:

nssm.exe remove myservice

### Some recommended bundled libraries to help build your service

pyodbc - database connectivity
schedule - schedule subprocesses to run on regular basis
simplejson - json parsing
requests - make http requests
rollbar - error reporting
datadog - timeseries data graphs/monitoring