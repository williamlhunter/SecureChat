# SecureChat
An end to end encrypted, peer to peer, terminal based chat client.  A first attempt at writing secure software.
## HAS NOT BEEN AUDITED BY ANYONE, USE AT YOUR OWN RISK

First client should run with no console arguments to start as a server.
Second client runs the script with their partner's ip address as an argument.
communicates over ports 5555 and 5556

Requires the following python packages:
* pyzmq
* cryptography
