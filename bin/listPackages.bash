#~/bin/bash
#
# List installed packages in chronological order of installation
#
for x in $(ls -1t /var/log/dpkg.log*); do zcat -f $x |tac |grep -e " install " -e " upgrade "; done |awk -F ":a" '{print $1 " :a" $2}' |column -t
#for x in $(ls -1t /var/log/dpkg.log*); do zcat -f $x |tac |grep -e " install " -e " upgrade "; done | column -t

