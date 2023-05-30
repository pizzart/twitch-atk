# twitch chat asobo chaos script
## description
pretty much says it all in the title. twitch chat can use commands to control an asobo game (any game that is supported by [ATK](https://github.com/widberg/atk)) in real time. use `!atk <command>` in chat, where `<command>` is a command that can be called using `runCommand()` in ATK (like SetTimeFactor 2, for instance)
## how to set up
- install python with pip (if on windows also check "add python to path" during install)
- install the dependencies for atk and my script using `pip install frida-tools twitchAPI` in the command line. if you're on windows run the command line as an administrator
- download the script and put it in some folder
- download [atk.js](https://github.com/widberg/atk/blob/master/atk.js) and put it in that folder
- now register an application on the [developer console](https://dev.twitch.tv/console)
- add `http://localhost:17563` as an oauth redirect url. the name doesn't matter
- copy the client id and replace the `APP_ID` variable in the script with it
- copy the client secret and paste it into an empty file called `token.txt` in that same folder (make sure the file only has a single line in it)
- also make sure to replace the `TARGET_CHANNEL` in the script with your own twitch username
- you should be ready to go
## credits
- https://github.com/widberg - for creating ATK (literally the backbone of this script)
- https://github.com/Geljado - for creating ATK-UI (code for communicating with ATK is from there lol)
