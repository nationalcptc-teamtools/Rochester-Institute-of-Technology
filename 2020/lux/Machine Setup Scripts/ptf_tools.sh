cd /opt/ptf
./ptf <<EOF
use metasploit
run
use wfuzz
run
use hydra
run
use owaspzsc
run
use gobuster
run
EOF


