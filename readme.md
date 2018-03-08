# Introduction
The following instructions explain how I managed to use my Logitech C270 usb webcam within a docker container for video streaming. I used:
- VirtualBox for the driver, 
- docker-machine to spin up docker hosts, and 
- docker for containers

#Install the Virtualbox Extension Pack via https://www.virtualbox.org/wiki/Downloads

# create the VM from the custom boot2docker iso:
docker-machine create -d virtualbox --virtualbox-boot2docker-url https://github.com/Alexoner/boot2docker/releases/download/v17.06.0-ce-usb-rc5/boot2docker.iso "VM name"

# stop the VM:
```docker-machine stop "VM name"```

# activate the USB controller:
```vboxmanage modifyvm "VM name" --usbxhci on```

# start the VM:
```docker-machine start "VM name"```

# check if the webcam is listed by virtualbox:
```VBoxManage list webcams```

# attach the webcam, identified by its alias, to the VM "VM name"
```VBoxManage controlvm "VM name" webcam attach .1```

# check that the webcam is attached:
```VBoxManage controlvm "VM name" webcam list```

# ssh into the VM and check if /dev/video0 exists:
```
docker-machine "VM name" ssh
ll /dev/video0
exit
```

# activate the environment of the VM via docker-machine, make sure it is active:
```
docker-machine env "VM name" | Invoke-Expression
docker-machine active
```

# make sure the docker-compose file contains a line that maps the /dev/video0 on the VM to /de/video0 in the docker container:
```
devices: 
    - /dev/video0:/dev/video0
```
# spin up the docker containers:
```docker-compose -f xxx up -d --build```

# check if the video stream works.

# useful links:
- https://forums.virtualbox.org/viewtopic.php?f=7&t=83397
- http://gw.tnode.com/docker/docker-machine-with-usb-support-on-windows-macos/
- https://stackoverflow.com/questions/41023827/accessing-usb-webcam-hosted-on-os-x-from-a-docker-container?rq=1
- https://www.virtualbox.org/manual/ch09.html#webcam-passthrough
- https://medium.com/@QuantuMobile/remote-video-streaming-with-face-detection-d52ce2d71419