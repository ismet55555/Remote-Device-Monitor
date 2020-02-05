<h1 align="center">Device Monitor :eyes:</h1>

This web application is used to monitor a remote target at a specified IP address (and/or port).
Essentially, you install this web application onto a device that will at regular interval ping the remote address
to see if it is online or offline.

There is a simple web interface for this monitoring application located at your devices local IP address,
and at port *7777*.  

For example, this web application can be accessed within the device at any of the following:
- http://localhost:7777
- http://0.0.0.0:7777/
- http://127.0.1.1:7777/ 

To run this web application run the bash script:
- `$ ./start`

Or it can be accessed from a seperate device on the same network at:
- http://[Monitor-Device-IP-Address-Here>:7777

**NOTE**: This is a work in progress and all specified parameters are static

## :bust_in_silhouette: Contributors
**Ismet Handžić** - Github: [@ismet55555](https://github.com/ismet55555)


## Licence
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
