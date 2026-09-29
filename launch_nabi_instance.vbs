' Silent Launcher for Antigravity Instance (nabistudii0@gmail.com)
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)
Cmd = "pythonw """ & ScriptDir & "\server.py"" --launch-instance nabistudii0@gmail.com"
WshShell.Run Cmd, 0, False
