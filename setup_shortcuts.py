import os
import subprocess
import chatgpt_account_manager as cpm

exe = cpm.get_chatgpt_exe_path() or r'C:\Program Files\WindowsApps\OpenAI.Codex_26.930.3930.0_x64__2p2nqsd0c76g0\app\ChatGPT.exe'
print('ChatGPT.exe path:', exe)

vbs_path = os.path.abspath('launch_chatgpt_enhanced.vbs')
vbs_inst2 = os.path.abspath('launch_chatgpt_instance2.vbs')
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
start_menu = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')

ps_script = f'''
$sh = New-Object -ComObject WScript.Shell

$sc1 = $sh.CreateShortcut('{os.path.join(desktop, "ChatGPT Enhanced.lnk")}')
$sc1.TargetPath = 'wscript.exe'
$sc1.Arguments = '"{vbs_path}"'
$sc1.WorkingDirectory = '{os.path.dirname(vbs_path)}'
$sc1.IconLocation = '{exe},0'
$sc1.Description = 'ChatGPT Desktop with Codex Pro & Persian UI Suite'
$sc1.Save()

$sc2 = $sh.CreateShortcut('{os.path.join(start_menu, "ChatGPT Enhanced.lnk")}')
$sc2.TargetPath = 'wscript.exe'
$sc2.Arguments = '"{vbs_path}"'
$sc2.WorkingDirectory = '{os.path.dirname(vbs_path)}'
$sc2.IconLocation = '{exe},0'
$sc2.Description = 'ChatGPT Desktop with Codex Pro & Persian UI Suite'
$sc2.Save()

$sc3 = $sh.CreateShortcut('{os.path.join(desktop, "ChatGPT Instance 2.lnk")}')
$sc3.TargetPath = 'wscript.exe'
$sc3.Arguments = '"{vbs_inst2}"'
$sc3.WorkingDirectory = '{os.path.dirname(vbs_inst2)}'
$sc3.IconLocation = '{exe},0'
$sc3.Description = 'ChatGPT Desktop Instance 2 (Isolated Account)'
$sc3.Save()
'''

r = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
print('Shortcut setup returncode:', r.returncode)
if r.stderr:
    print('stderr:', r.stderr)
else:
    print('Successfully updated Desktop and Start Menu shortcuts!')
