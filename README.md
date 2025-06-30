# Network Device Status and Notification Device 

**Author:** Max Porseryd (mp224hv)  
**Course:** 1DT305 - Introduction to Applied Internet of Things 
**Date:** June 2025

## Project Overview

I built a network monitoring system using a Raspberry Pi Pico W that watches my home network devices and shows their status with colored LEDs. It keeps an eye on my server, PC, and specific services on the server like Jellyfin, then lights up green when everything's working or red when something's down. 

It hosts an HTTP API, so other systems can send it notifications to trigger different LED patterns. Useful for seeing at a glance if my home lab is having issues without having to check a bunch of different dashboards or log into anything, its just right there on my wall. Currently i have four levels of notifications, none (led of), info (on), warning (slowly blinking) and critical (triple blink every couple of seconds). 

Another feature is a temperature sensor on the pico that reads the room temperature which is retrievable from the HTTP API, this is a bit of a tack on because of the course requirements but it will come in handy as i dont have another temperature sensor anywhere in my appartment. 


**Estimated completion time:**  

## Objective

### Why This Project?

Honestly, I got tired of my server randomly going down and not knowing about it until I tried to use something. I wanted something simple that would just tell me "hey, your stuff is broken" without having to open up some webpage or other monitoring tool, just a quick glance at my wall or whereever i put this and know if i need to log into a device to fix or look at something.

### Purpose and Benefits

The main goals were:
- Quick visual feedback - I can just glance at the LEDs and know if something's wrong
- Catch problems early - Better to know about issues before they affect what I'm doing
- Monitor specific services - Not just "is the server on" but "is Jellyfin actually running"
- Accept external notifications - Other scripts can tell it to flash lights for warnings so i can know if my server is overheating or something else. 
- Learn - Good excuse to play with async programming and IoT concepts.

### Expected Insights

The system provides insights into:
- How my networked devices are doing, if they are up and if they have any important notifications/events. 
- Current temperature of my apartment

## Material

### Components Used

| Component | Purpose | Specifications | Source | 
|-----------|---------|----------------|---------|
| Raspberry Pi Pico W | Main microcontroller | ARM Cortex-M0+, 264KB RAM, WiFi | Electrokit |
| LEDs (Red/Green/Yellow) | Status indicators | 3mm, 20mA, 2.0-2.2V forward voltage | Electrokit |
| Resistors | Current limiting | 1000Ω | Electrokit |
| Breadboard | Wiring Platform | 840 connection points | Electrokit |
| Jumper wires | Connections | Male-to-male, various colors | Electrokit |
| USB Cable | Programming/Power | Micro-USB to USB-A | Electrokit |
| MCP9700 TO-92 Temperature Sensor | Read the temprerature | 2.3-5.5VDC | Electrokit |

**Total Cost: 349kr** (for the start kit bundle) + shipping 

### Component Details

**Raspberry Pi Pico W:** The heart of the system, chosen for its built-in WiFi capability, sufficient GPIO pins for multiple LEDs, and native MicroPython support. 

**LEDs:** Standard 3mm LEDs provide clear visual indication. Colors chosen follow common conventions:
- Red: Device/service down or error state
- Green: Device/service operational
- Yellow: Warning/notification state

**Resistors:** 1000Ω resistors limit current to safe levels for LEDs, ensuring longevity and preventing damage.

**Temperature Sensor**: Reads the ambient temperature.

## Computer Setup

### Development Environment

My development environment is centered around **Neovim**. I use it as my main editor alongside a Python LSP for code intelligence.

When working with MicroPython, I don’t use any special plugins just a standard Python LSP. To interface with the Raspberry Pi Pico, I use **mpremote**, a terminal tool that makes it easy to upload files and access the Pico REPL.

For managing project-specific dependencies like mpremote or python3, I use nix-shell. Each project includes a shell.nix file that declares the necessary packages. When I run nix-shell, the required tools are installed in a temporary isolated environment. This ensures that all dependencies are tied directly to the project, making it easy to get started, just enter the development shell and everything is ready to go.

If you're curious, you can explore my full setup here: https://github.com/mxapd/nix.

### Installation Steps

#### IDE and development environment
Installing and configuring neovim is not something i want to go into here since it goes outside the scope for this report. All my configuration files can be found in my nix repo above. 

To install python and mpremote i use a nix-shell as mentioned, to follow along with that method all you need to do is copy that file, put it in your project directory and run $ nix-shell. 

(OBS requires you to be on nixos or have the nix package manager, if you dont want to do that just install in some other way) 

While in the development shell python and mpremote are availible to use. 

#### Setting up Pico for MicroPython

Next is setting up and preparing the pico for programming with micropython.  

1. Download the firmware from https://micropython.org/download/RPI_PICO_W/
2. Plug in your microUSB cable into the pico and then hold BOOTSEL while plugging it in to a computer.
3. Copy the .uf2 file into the mass storage device that appears. The pico will now install the firmware and automaticly reset, after which it is ready for use.

Now to upload code all we need to do is use mpremote, the exact command to copy files is ``=bash
mpremote connect auto fs cp <filename> : # copy files to pico
mpremote connect auto repl # connect to the repl to run commands
``
If it doesnt work try with sudo.

## Putting Everything Together

### Circuit Design

```
Pico W GPIO Layout:
├── Pin 2  → 1000Ω → Red LED   (Server status)
├── Pin 3  → 1000Ω → Green LED (Server status)  
├── Pin 4  → 1000Ω → Yellow LED (Server notifications)
├── Pin 6  → 1000Ω → Red LED   (PC status)
├── Pin 7  → 1000Ω → Green LED (PC status)
├── Pin 8  → 1000Ω → Yellow LED (PC notifications)
├── Pin 10 → 1000Ω → Green LED (Jellyfin service)
├── Pin 11 → 1000Ω → Red LED   (Jellyfin service)
├── Pin 14 → 1000Ω → Green LED (Web service)
├── Pin 15 → 1000Ω → Red LED   (Web service)
└── GND    → Common ground for all LEDs
```

### Electrical Calculations

## Platform Choice

### How I Set Things Up

### Why This Way?

### If I Wanted to Scale

### Platform Benefits

### Scaling Considerations

## The Code

### How It Works/Design/Architecture

## How Data Gets Around

### Monitoring Schedule

### Network Protocols

### Why These Choices

## How the Status Display Works

### The LED Dashboard

### Data Storage (Or Lack Thereof)

### Future Ideas

## Final Results

### What Actually Works

### How It Went

### What I Learned

---

**Code Repository:** https://github.com/mxapd/IoT_server_status  
