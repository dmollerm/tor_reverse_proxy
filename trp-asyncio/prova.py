
import logging
import sys
import socks
import socket
def getaddrinfo(*args):
    _logger.debug("calling getaddrinfo")
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo
import asyncio

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger('tor_reverse_proxy')



def get_tor_socket():
    _socket = socks.socksocket()
    _socket.set_proxy(socks.SOCKS5, 'gateway', 9050)
    _logger.debug("mocking getaddrinfo")
    _socket.getaddrinfo = getaddrinfo
    return _socket


def get_socket():
    return socket.socket()


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    _logger.debug("Connection from %r" % (addr,))

    loop = asyncio.get_event_loop()

    _socket = get_tor_socket()
    #await loop.sock_connect(_socket, ('www.dnsdynamic.org', 80))
    await loop.sock_connect(_socket, ('msydqstlz2kzerdg.onion', 80))

    _logger.debug("Connected?")

    if True:
        reqs = await reader.read(1024)
        if reqs:
            _logger.debug("forwardin request %s", reqs)
            await loop.sock_sendall(_socket, reqs)
        else:
            _logger.debug("empty request")
            #break

    _logger.debug("Resp forwarded")


    while True:
        resp = await loop.sock_recv(_socket, 1024)
        if resp:
            _logger.debug("forwardin response %s", resp)
            writer.write(resp)
        else:
            _logger.debug("empty response")
            _socket.close()
            break

    await writer.drain()

    _logger.debug("Close the client socket")

    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '0.0.0.0', 8000, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
_logger.info('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
