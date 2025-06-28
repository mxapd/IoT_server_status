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
| MCP9700 TO-92 Temperaturgivare | Read the temprerature | 2.3-5.5VDC | Electrokit |

**Total Cost: 349kr** + shipping (for the start kit bundle)

### Component Details

## Computer Setup

### Development Environment

### Installation Steps

## Putting Everything Together

### Circuit Design

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
