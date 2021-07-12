#~/bin/bash

export REPO=/home/ipfs/.ipfs

# Check if IPFS init.log exists and has a peer id. Return 1 if YES
if [ -f $REPO/init.log ]; then
  grep -ic 'peer identity:' $REPO/init.log
else
  echo '0'
fi
