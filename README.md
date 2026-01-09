# Terminal Confetti 🎉

A lightweight Python script that displays a colorful confetti animation directly in your terminal.

## Features
- Uses ANSI escape codes for color and cursor control
- Adapts to terminal size automatically
- Smooth falling animation with random sway
- Restores terminal state on exit
- No external dependencies

## Requirements
- Python 3.x
- A terminal that supports ANSI escape sequences

## APT Integration (Debian/Ubuntu)

To run the confetti animation automatically after APT operations, create the following configuration file:

```bash
sudo nano /etc/apt/apt.conf.d/99confetti
```

```bash
DPkg::Post-Invoke { "python3 /usr/local/bin/confetti.py"; };
APT::Update::Post-Invoke-Success { "python3 /usr/local/bin/confetti.py"; };
