# tor_reverse_proxy
Reverse proxy for hidden services

This software is intended to serve as reverse proxy for tor hidden services.

Its main goal is to permit that someone keeps a backend completely
hidden in the tor network but a third party hosts this proxy in the clear net.

This will allow
- to index the hidden service
- to keep the backend administrator private
- to speed up the browsing experience
- to firewall the backend much earlier against malicious requests

This architecture is intended only for those services whose publisher is at risk,
while the client can visit the site with no privacy concerns. I.e. clandestine newspapers, leak sites, blogs...

The hidden backend admin should completely trust the reverse proxy
operator: the latter will always be running a complete man in the middle!
Still, the backend admin interface should *not* be accessed through the reverse proxy.
