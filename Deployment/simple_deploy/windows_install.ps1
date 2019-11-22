Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

choco install -y googlechrome
choco install -y burp-suite-free-edition
choco install -y firefox
choco install -y git.install
choco install -y sublimetext3.app
