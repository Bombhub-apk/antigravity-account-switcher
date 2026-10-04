Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
strPrograms = WshShell.SpecialFolders("Programs")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' 1. Desktop - ChatGPT Enhanced
Set oLnk1 = WshShell.CreateShortcut(strDesktop & "\ChatGPT Enhanced.lnk")
oLnk1.TargetPath = strPath & "\launch_chatgpt_enhanced.vbs"
oLnk1.WorkingDirectory = strPath
oLnk1.Description = "ChatGPT Desktop with Persian fonts, custom theme and account switcher"
oLnk1.Save

' 2. Desktop - ChatGPT Instance 2
Set oLnk2 = WshShell.CreateShortcut(strDesktop & "\ChatGPT Instance 2.lnk")
oLnk2.TargetPath = strPath & "\launch_chatgpt_instance2.vbs"
oLnk2.WorkingDirectory = strPath
oLnk2.Description = "ChatGPT Desktop Instance 2 (Isolated Account)"
oLnk2.Save

' 3. Start Menu Programs - ChatGPT Enhanced
Set oLnk3 = WshShell.CreateShortcut(strPrograms & "\ChatGPT Enhanced.lnk")
oLnk3.TargetPath = strPath & "\launch_chatgpt_enhanced.vbs"
oLnk3.WorkingDirectory = strPath
oLnk3.Description = "ChatGPT Desktop with Persian fonts, custom theme and account switcher"
oLnk3.Save

WScript.Echo "All shortcuts created successfully."
