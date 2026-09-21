' Antigravity Switcher Silent Windows Launcher
' Author: Ethan Carter (https://github.com/Bombhub-apk/antigravity-account-switcher)
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)
ServerScript = Chr(34) & ScriptDir & "\server.py" & Chr(34)
WshShell.Run "pythonw " & ServerScript, 0, False
