Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c ""cd C:\Users\HP\Desktop\Spese mensili && python gestore_spese.py""", 0, false
Set WshShell = Nothing