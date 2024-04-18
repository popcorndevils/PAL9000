# To start the session
$ screen -S screen_name
# To resume the session or Reattach session enters a screen process
$ screen -r
# If there will be multiple screen running then 
$ screen -r screen_name
# To detach the session
$ screen –d screen_name
# View all screen sessions
$ screen -ls
After entering the screen session, you can create multiple windows in the session and manage the windows. The management command starts with ctrl+ a

ctrl + a + c: create a new window (create)
ctrl + a + n: switch to the next window (next)
ctrl + a + p: switch to the previous window (previous)
ctrl + a + w: list all windows
ctrl + a + A: Rename window
ctrl + a + d: detach the current session
ctrl + a + [1-9]: switch to the specified window (1-9 is the window number)
ctrl + d: Exit (close) the current window
Multi-Window: In the Screen environment, all sessions run independently, and have their own number, input, output, and window cache. Users can switch between different windows through shortcut keys, and can freely redirect the input and output of each window. Screen implements basic text operations, such as copy and paste, etc. It also provides a scroll bar-like function to view the history of the window status. The window can also be partitioned and named, and the activity of the background window can be monitored.
Session Sharing: Screen allows one or more users to log in to a session multiple times from different terminals and share all the characteristics of the session (for example, you can see exactly the same output). It also provides a mechanism for window access authority, which can password protect the window.
New window
There are 3 ways to create a new window:

$ screen #In this way, you can create a new window and enter a window, but then the window has no name, and cannot distinguish between them

$ screen -S name #This creates a new window named name and merges it into the window

For example screen -S count creates a new window called count and enters

$ screen command #This creates a new window and executes the command in the window, also without a name

For example screen python ./sample.py Create and execute sample.py program

Other Useful Screen Commands
# Terminate Screen session, If the session is no longer needed, just kill it. To kill the disconnected session named senthil:
screen -r sample -X quit
or:
screen -X -S sample quit
or:
screen -X -S 29415 quit
********************************************************************
Ctrl + a :list all conversations
Ctrl + a 0 :switch to session number 0
Ctrl + an :switch to the next session
Ctrl + ap :switch to the previous session
Ctrl + a S :Split the current area into two areas horizontally
Ctrl + al :Split the current area into two areas vertically
Ctrl + a Q :Close all sessions except the current session
Ctrl + a X :close the current session
Ctrl + a \ :Terminate all sessions and terminate Screen
Ctrl + a? :Show key bindings. To log out, press enter #### Lock session
******************************************************************
# Screen has an option to lock the session. To do this, press Ctrl + a and x. Enter your Linux password to lock it.
Screen used by sk on ubuntuserver.
Password:
# Record session
You may want to record everything in the Screen session. To do this, just press Ctrl + a and H.
# Alternatively, you can use the -L parameter to start a new session to enable logging.
screen -L
From now on, all the activities you do in the session will be recorded and stored in a file named screenlog.x in the $HOME directory. Here, x is a number.
You can use the cat command or any text viewer to view the contents of the log file.
Kill the session window
If you want to close an extra window, there are 3 ways:

kill -9 threadnum For example, in the 2637 above, kill -9 2637 can kill the thread, and of course it kills the window

Use Ctrl a +k to kill the current window and the programs running in the window

Use Ctrl a and enter the quit command to exit the Screen session. It should be noted that this exit will kill all windows and exit all running programs

Clear dead windows
When the window is killed, you can use screen -ls to see (???dead) behind the window, indicating that the window is dead, but still occupying space. At this time you need to clear the window

$ screen -wipe #Automatically clear dead windows

This kind of window is clear~

If there is no open session, you will see the following output:

$ screen -ls

No Sockets found in /run/screens/S-sk.

For more details, please refer to the man page:

$ man screen