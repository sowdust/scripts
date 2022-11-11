LAST=`curl -s https://gitweb.torproject.org/tor.git/plain/ChangeLog 2> /dev/null | head -1 | sed 's/.*version //' | cut -d ' ' -f 1`
CURR=`tor --version | head -1 | sed 's/.*version //' | sed s'/\.$//'`

if [[ $LAST = $CURR ]]
then
	exit 0
fi

echo "Upgrading to Tor version $LAST from $CURR"
URL="https://dist.torproject.org/tor-$LAST.tar.gz"

cd /tmp
wget $URL
tar xfvz tor-$LAST.tar.gz
cd tor-$LAST
./configure --disable-asciidoc
make
make install
echo "Upgraded Tor to version $LAST from $CURR"
reboot