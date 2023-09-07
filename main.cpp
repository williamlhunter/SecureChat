#include <iostream>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#define DEFAULT_PORT "9999"
#define HELP_OUTPUT "placeholder"

using namespace std;

int main(int argc, char *argv[])
{
    int socket_handle;
    int status;
    int errno;
    struct addrinfo hints;
    struct addrinfo *partner;
    
    //check if arguments are supplied correctly
    if (argc != 2)
    {
        cout << HELP_OUTPUT << endl;
        return 1;
    } else if (!strcmp(argv[1], "-h"))
    {
        cout << HELP_OUTPUT << endl;
        return 0;
    }

    //initialize an addrinfo 
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;
    if ((status = getaddrinfo(argv[1], DEFAULT_PORT, &hints, &partner)) != 0) {
        cout << "getaddrinfo error: " << gai_strerror(status) << endl;
        cout << "Did you supply a valid IP address?" << endl;
        return 1;
    }

    //initialize a socket descriptor
    socket_handle = socket(partner->ai_family, partner->ai_socktype, partner->ai_protocol);
    if (socket_handle == -1)
    {
        cout << "could not create socket" << endl;
        return 1;
    }

    freeaddrinfo(partner);

    return 0;
}
