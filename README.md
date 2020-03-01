<h1 align="center">Remote Device Monitor :eyes:</h1>

This linux based web application is used to monitor a remote targets at a specified IP address (IPv4) at specified port numbers.

Essentially, you install this web application onto any linux device (or linux container) that will at regular interval ping the specified remote addresses to see if it is online or offline.

This remote device monitor has a simple web interface that shows the status of the monitored addresses. This web interface can be accessed through any common web browswer at the device monitor's host IP address, and at port *7777*.  

# :computer: Web Interface
For example, this web interface can be accessed within the web browser on the host device at any of the following:
- http://localhost:7777
- http://0.0.0.0:7777/
- http://127.0.1.1:7777/ 

However, if wanting to access the web interface from anywhere on the same/local network from any other device, you can access it with `http://<IP Address of Host Device>:7777`

# :rocket: Installing and Setup
## Using Bash Script
After you cloan this repository, you can run this web application run the following bash script. This bash script will automatically create a virtual environment and install all needed dependencies.
- `$ ./start`

## Using Docker
The provided [`Dockerfile`](Dockerfile) has been configured specifically for a *Raspberry Pi*, however you can change the initial `FROM` parameter to any Debian based image with a python base (see Dockerhub). 
 
# :warning: Note
This is a work in progress and all specified parameters are static. As of now, the target device IP addresses and port numbers are entered in [`app/routes.py`](app/routes.py) by adding another Monitor object.

## :bust_in_silhouette: Contributors
**Ismet Handžić** - Github: [@ismet55555](https://github.com/ismet55555)

## Licence
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
