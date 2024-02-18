# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is power supply controller implementation of TDK-Lambda PS with ATEN RS-232 to USB adapter 

### How do I get set up? ###

* pip install opsys-ps-controller

### Unit Testing

* python -m unittest -v

### Usage Example
```
from opsys_ps_controller.ps_controller import PsController

ps_conn = PsController()

ps_conn.init_connection()
ps_conn.ps_on()
ps_conn.disconnect()
```