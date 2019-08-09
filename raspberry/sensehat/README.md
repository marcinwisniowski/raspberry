# Raspberry Pi Sense HAT

This module contains example exercises and programs to execute on Sense HAT

## Setup

To setup SenseHAT few steps need to be done to make the HAT work properly

### 1. Install the Hardware

It a crucial to plug the SenseHAT properly it means to push GPIO to the end. Next step is secure the pins with plastic 
screws shipped with the package. Once it is plugged and secured next steps can be followed.

**NOTE:** *Not properly hardware setup is first step to check if SenseHAT fails*  

### 2. Enable interfaces

Sense HAT requires I²C or SPI interfaces to work.
Enabling that can be done with Graphical GUI:

Home > Preferences > Raspberry Pi Configuration

Alternative way is to edit raspberrypi core modules configuration file:

```bash
sudo vi /boot/config.txt
```

Uncoment `i2c_arm`  and `spi`

```
# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on
#dtparam=i2s=on
dtparam=spi=on
```

After reboot of the PI few verification steps can be performed:

```bash
ls /dev/i2c*
```
If none is return, it means that I²C interface was not initialized.

```bash
i2cdetect -y 1
```

If the address matrix contains all 00 means that I²C components on the Sense HAT has no connection with RaspberryPi


### 3. Set GPIO Layout

Load SenseHAT module using `dtoverlay` routine. This one is required if by default Raspberry Pi can not properly read
the EEPROM ID form the SenseHAT. This operation can be done by editing the `/boot/config.txt` file 

```bash
sudo vi /boot/config.txt
```

Add this line in the lower sections of config file 

```
# Enable SenseHat
dtoverlay=rpi-sense
```

Reboot just after saving

## Troubleshooting

https://lb.raspberrypi.org/forums/viewtopic.php?t=192033#p1358735
