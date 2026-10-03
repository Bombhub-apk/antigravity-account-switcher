Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

Set oShellLink = WshShell.CreateShortcut(strDesktop & "\ChatGPT Enhanced.lnk")
oShellLink.TargetPath = strPath & "\launch_chatgpt_enhanced.vbs"
oShellLink.WorkingDirectory = strPath
oShellLink.Description = "ChatGPT Desktop with Persian fonts and themes"
oShellLink.Save

Set oShellLink2 = WshShell.CreateShortcut(strDesktop & "\ChatGPT Instance 2.lnk")
oShellLink2.TargetPath = strPath & "\launch_chatgpt_instance2.vbs"
oShellLink2.WorkingDirectory = strPath
oShellLink2.Description = "ChatGPT Desktop Instance 2"
oShellLink2.Save

WScript.Echo "Shortcuts created successfully."
