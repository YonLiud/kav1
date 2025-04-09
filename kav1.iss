[Setup]
AppName=Kav1 App
AppVersion=1.0
DefaultDirName={pf}\Kav1
OutputDir=.
OutputBaseFilename=kav1_setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "backend\dist\server\server.exe"; DestDir: "{app}\server"; Flags: ignoreversion
Source: "backend\dist\server\_internal\*"; DestDir: "{app}\server\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

Source: "frontend\dist\main\main.exe"; DestDir: "{app}\client"; Flags: ignoreversion
Source: "frontend\dist\main\_internal\*"; DestDir: "{app}\client\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Kav1 Frontend"; Filename: "{app}\main.exe"
Name: "{group}\Kav1 Backend"; Filename: "{app}\server.exe"
