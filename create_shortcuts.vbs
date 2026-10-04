Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
strPrograms = WshShell.SpecialFolders("Programs")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

Set fso = CreateObject("Scripting.FileSystemObject")
strIcon = ""
On Error Resume Next
Set oExec = WshShell.Exec("powershell -NoProfile -Command ""(Get-Item 'C:\Program Files\WindowsApps\OpenAI.Codex_*\app\ChatGPT.exe' -ErrorAction SilentlyContinue | Select-Object -Last 1).FullName""")
If Not oExec Is Nothing Then
    strIcon = Trim(oExec.StdOut.ReadAll())
End If
On Error GoTo 0

' 1. Desktop - ChatGPT Enhanced
Set oLnk1 = WshShell.CreateShortcut(strDesktop & "\ChatGPT Enhanced.lnk")
oLnk1.TargetPath = strPath & "\launch_chatgpt_enhanced.vbs"
oLnk1.WorkingDirectory = strPath
If strIcon <> "" And fso.FileExists(strIcon) Then
    oLnk1.IconLocation = strIcon & ", 0"
End If
oLnk1.Description = "ChatGPT Desktop with Persian fonts, custom theme and account switcher"
oLnk1.Save

' 2. Desktop - ChatGPT Instance 2
Set oLnk2 = WshShell.CreateShortcut(strDesktop & "\ChatGPT Instance 2.lnk")
oLnk2.TargetPath = strPath & "\launch_chatgpt_instance2.vbs"
oLnk2.WorkingDirectory = strPath
If strIcon <> "" And fso.FileExists(strIcon) Then
    oLnk2.IconLocation = strIcon & ", 0"
End If
oLnk2.Description = "ChatGPT Desktop Instance 2 (Isolated Account)"
oLnk2.Save

' 3. Start Menu Programs - ChatGPT Enhanced
Set oLnk3 = WshShell.CreateShortcut(strPrograms & "\ChatGPT Enhanced.lnk")
oLnk3.TargetPath = strPath & "\launch_chatgpt_enhanced.vbs"
oLnk3.WorkingDirectory = strPath
If strIcon <> "" And fso.FileExists(strIcon) Then
    oLnk3.IconLocation = strIcon & ", 0"
End If
oLnk3.Description = "ChatGPT Desktop with Persian fonts, custom theme and account switcher"
oLnk3.Save

WScript.Echo "All shortcuts created successfully."

