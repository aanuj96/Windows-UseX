# ⚡ Terminal Commands Quick Reference

## 🚀 Quick Access Guide

**Use this as a cheat sheet for Terminal-First Mode!**

---

## 📂 File Operations

```powershell
# CREATE
New-Item file.txt -ItemType File
"content" | Set-Content file.txt
mkdir newfolder

# READ
Get-Content file.txt
cat file.txt                    # Alias
Get-Content file.txt -First 10  # First 10 lines
Get-Content file.txt -Tail 10   # Last 10 lines

# COPY
Copy-Item file.txt backup.txt
Copy-Item *.txt backup\
cp file.txt backup.txt          # Alias

# MOVE/RENAME
Move-Item old.txt new.txt
mv old.txt new.txt              # Alias
Rename-Item old.txt new.txt

# DELETE
Remove-Item file.txt
rm file.txt                     # Alias
Remove-Item *.tmp -Recurse -Force

# FIND
Get-ChildItem -Recurse -Filter "*.txt"
ls -R *.txt                     # Alias
Select-String "text" *.txt      # Search in files
```

---

## 🖥️ Application Management

```powershell
# LAUNCH
Start-Process notepad
Start-Process chrome
Start-Process explorer "C:\folder"
Start-Process "app.exe" -ArgumentList "/arg"

# CLOSE
Stop-Process -Name notepad
Get-Process chrome | Stop-Process
taskkill /IM notepad.exe /F

# LIST
Get-Process
Get-Process | Where-Object {$_.Name -like "*chrome*"}
ps | grep chrome                # Unix-style

# CHECK IF RUNNING
Get-Process notepad -ErrorAction SilentlyContinue
if (Get-Process notepad -EA SilentlyContinue) { "Running" }
```

---

## 📁 Directory Operations

```powershell
# NAVIGATE
Set-Location C:\Users
cd C:\Users                     # Alias
Push-Location C:\temp           # Save location
Pop-Location                    # Return to saved

# LIST
Get-ChildItem
ls                              # Alias
dir                             # Alias
ls -Force                       # Show hidden
ls -Recurse                     # Recursive

# CREATE
New-Item -Path "folder" -ItemType Directory
mkdir folder                    # Alias
md folder                       # Alias

# CURRENT PATH
Get-Location
pwd                             # Alias
$PWD.Path

# CHECK EXISTS
Test-Path "C:\folder"
if (Test-Path "file.txt") { "Exists" }
```

---

## 📝 Text Manipulation

```powershell
# WRITE
"text" | Set-Content file.txt
"text" > file.txt
echo "text" | Out-File file.txt

# APPEND
"text" | Add-Content file.txt
"text" >> file.txt

# REPLACE
(Get-Content file.txt) -replace "old", "new" | Set-Content file.txt

# SEARCH
Select-String "pattern" file.txt
Select-String "pattern" *.txt -Recurse

# COMBINE
Get-Content file1.txt, file2.txt | Set-Content combined.txt

# COUNT LINES
(Get-Content file.txt).Count

# SORT
Get-Content file.txt | Sort-Object
Get-Content file.txt | Sort-Object -Unique

# FILTER
Get-Content file.txt | Where-Object {$_ -like "*pattern*"}
```

---

## 🌐 Network Operations

```powershell
# PING
Test-Connection google.com
ping google.com

# WEB REQUEST
Invoke-WebRequest "https://api.example.com"
curl "https://api.example.com"  # Alias

# DOWNLOAD FILE
Invoke-WebRequest "https://example.com/file.zip" -OutFile "file.zip"
wget "https://example.com/file.zip" -O "file.zip"

# DNS LOOKUP
Resolve-DnsName google.com
nslookup google.com

# IP CONFIG
Get-NetIPAddress
ipconfig

# PORT TEST
Test-NetConnection -ComputerName google.com -Port 443
```

---

## ⚙️ System Information

```powershell
# COMPUTER INFO
Get-ComputerInfo
$env:COMPUTERNAME
hostname

# USER INFO
$env:USERNAME
$env:USERPROFILE
whoami

# OS INFO
Get-CimInstance Win32_OperatingSystem
systeminfo

# DISK INFO
Get-PSDrive
Get-Volume
Get-Disk

# MEMORY
Get-CimInstance Win32_PhysicalMemory
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory

# CPU
Get-CimInstance Win32_Processor
wmic cpu get name

# ENVIRONMENT VARIABLES
Get-ChildItem Env:
$env:PATH
$env:TEMP
```

---

## 🔧 Registry Operations

```powershell
# READ
Get-ItemProperty "HKCU:\Software\Microsoft\..."
reg query "HKCU\Software\..." /v ValueName

# WRITE
Set-ItemProperty "HKCU:\..." -Name "Key" -Value "Value"
New-ItemProperty "HKCU:\..." -Name "Key" -Value "Value"
reg add "HKCU\..." /v Key /t REG_SZ /d "Value"

# DELETE
Remove-ItemProperty "HKCU:\..." -Name "Key"
reg delete "HKCU\..." /v Key
```

---

## 🛠️ Services

```powershell
# LIST
Get-Service
Get-Service | Where-Object {$_.Status -eq "Running"}

# START
Start-Service "ServiceName"
net start "ServiceName"

# STOP
Stop-Service "ServiceName"
net stop "ServiceName"

# RESTART
Restart-Service "ServiceName"

# STATUS
Get-Service "ServiceName" | Select-Object Status
sc query "ServiceName"
```

---

## 📦 Archives & Compression

```powershell
# ZIP
Compress-Archive -Path "folder" -DestinationPath "archive.zip"
Compress-Archive -Path "*.txt" -DestinationPath "files.zip"

# UNZIP
Expand-Archive -Path "archive.zip" -DestinationPath "folder"
Expand-Archive "archive.zip" "."

# UPDATE ZIP
Compress-Archive -Path "newfile.txt" -Update -DestinationPath "archive.zip"
```

---

## ⏰ Date & Time

```powershell
# CURRENT DATE/TIME
Get-Date
Get-Date -Format "yyyy-MM-dd"
Get-Date -Format "HH:mm:ss"

# FILE TIMESTAMPS
(Get-Item file.txt).LastWriteTime
(Get-Item file.txt).CreationTime

# CALCULATE
(Get-Date).AddDays(7)
(Get-Date).AddHours(-2)

# COMPARE
$date1 = Get-Date "2024-01-01"
$date2 = Get-Date
($date2 - $date1).Days
```

---

## 🔄 Loops & Automation

```powershell
# FOR EACH FILE
Get-ChildItem "*.txt" | ForEach-Object {
    Write-Host $_.Name
}

# FOR RANGE
1..10 | ForEach-Object {
    "Line $_" | Add-Content "file.txt"
}

# WHILE
$i = 1
while ($i -le 5) {
    Write-Host "Iteration $i"
    $i++
}

# DO-UNTIL
do {
    $input = Read-Host "Enter 'quit' to exit"
} until ($input -eq "quit")
```

---

## 🎯 Conditional Operations

```powershell
# IF-ELSE
if (Test-Path "file.txt") {
    "File exists"
} else {
    "File not found"
}

# SWITCH
switch ($value) {
    1 { "One" }
    2 { "Two" }
    default { "Other" }
}

# TERNARY (PowerShell 7+)
$result = (Test-Path "file.txt") ? "Exists" : "Not found"
```

---

## 📊 Data Formatting

```powershell
# TO CSV
Get-Process | Export-Csv "processes.csv"
Get-Service | ConvertTo-Csv | Out-File "services.csv"

# FROM CSV
Import-Csv "data.csv"
Import-Csv "data.csv" | ForEach-Object { $_.Name }

# TO JSON
@{Name="John"; Age=30} | ConvertTo-Json | Out-File "data.json"

# FROM JSON
$data = Get-Content "data.json" | ConvertFrom-Json
$data.Name

# TO XML
Get-Process | Export-Clixml "processes.xml"
$data = Import-Clixml "processes.xml"

# TABLE
Get-Process | Format-Table Name, CPU, Memory
Get-Process | Format-List *
```

---

## 🔐 Permissions & Security

```powershell
# FILE PERMISSIONS
Get-Acl "file.txt"
$acl = Get-Acl "file.txt"
Set-Acl "file.txt" $acl

# RUN AS ADMIN
Start-Process powershell -Verb RunAs
Start-Process "app.exe" -Verb RunAs

# EXECUTION POLICY
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎨 Window Management

```powershell
# MINIMIZE ALL
(New-Object -ComObject Shell.Application).MinimizeAll()

# TOGGLE DESKTOP
(New-Object -ComObject Shell.Application).ToggleDesktop()

# WINDOW CONTROL (requires additional module)
$shell = New-Object -ComObject WScript.Shell
$shell.SendKeys("^{ESC}")  # Win key
```

---

## 💡 Pro Tips

### **Combine Commands**
```powershell
# Create, edit, and save in one line
"Hello World" | Set-Content file.txt; Start-Process notepad file.txt
```

### **Use Aliases**
```powershell
ls = Get-ChildItem
cd = Set-Location
cp = Copy-Item
mv = Move-Item
rm = Remove-Item
cat = Get-Content
```

### **Pipeline Magic**
```powershell
# Find large files, copy to backup
Get-ChildItem -Recurse | 
    Where-Object {$_.Length -gt 10MB} | 
    Copy-Item -Destination "C:\backup\"
```

### **One-Liners**
```powershell
# Create 100 test files
1..100 | % { "Content $_" | Set-Content "file$_.txt" }

# Batch rename
Get-ChildItem *.jpg | % -Begin {$i=1} -Process { Rename-Item $_ "photo$i.jpg"; $i++ }
```

---

## 🎮 Quick Examples

### **Task: Create project structure**
```powershell
"src","tests","docs","config" | ForEach-Object { mkdir $_ }
"README.md","LICENSE",".gitignore" | ForEach-Object { New-Item $_ }
```

### **Task: Find and remove temp files**
```powershell
Get-ChildItem -Recurse -Filter "*.tmp" | Remove-Item -Force
```

### **Task: Backup with timestamp**
```powershell
$date = Get-Date -Format "yyyy-MM-dd_HHmm"
Compress-Archive -Path "project\" -DestinationPath "backup_$date.zip"
```

### **Task: Monitor file changes**
```powershell
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\folder"
$watcher.EnableRaisingEvents = $true
Register-ObjectEvent $watcher "Created" -Action {
    Write-Host "File created: $($Event.SourceEventArgs.Name)"
}
```

---

## 🚀 Remember

```
1. Shell Tool > Shortcut Tool > GUI Tools
2. Pipeline everything: Get-X | Where-Y | ForEach-Z
3. Tab completion is your friend
4. Get-Help cmdlet for details
5. Most commands have -WhatIf for testing
```

**Happy Terminal-First Automation!** ⚡🖥️

