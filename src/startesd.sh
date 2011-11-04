#start esd
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
echo "starting stream to $1"
esd -tcp -bind ::1 & 
sleep 2
(esdrec -s ::1 | esdcat -s "$1") &