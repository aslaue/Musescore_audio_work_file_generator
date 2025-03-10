$folder_dest = "$env:HOMEPATH\Downloads"

### Installation de python
$url = "https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe"
$file_dest = "$folder_dest\python3.13.2.exe"

Invoke-WebRequest -Uri $url -OutFile $file_dest

Start-Process -FilePath "$file_dest" -Wait

rm $file_dest

### installation de pip
$url = "https://bootstrap.pypa.io/get-pip.py"
$file_dest = "$folder_dest\get-pip.py"

Start-Process -FilePath "python" -ArgumentList "$file_dest" -Wait

rm $file_dest

### installation des librairies

Start-Process -FilePath "pip" -ArgumentList "install", "tk" -Wait

###
echo "L'installation s'est bien déroulée. Fermeture du programme"
Start-Sleep -Seconds 10
Exit





