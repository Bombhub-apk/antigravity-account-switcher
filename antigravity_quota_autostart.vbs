Set WshShell = CreateObject("WScript.Shell")
UserProfile = WshShell.ExpandEnvironmentStrings("%USERPROFILE%")
DaemonScript = Chr(34) & UserProfile & "\.gemini\antigravity\bin\sync_daemon.py" & Chr(34)
WshShell.Run "pythonw " & DaemonScript, 0, False
