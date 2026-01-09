#!/usr/bin/env python3
import random
import time
import shutil
import sys
import signal

def confetti_cannons():
    # 1. Setup Signals (Un-skippable)
    def handler(signum, frame):
        pass
    signal.signal(signal.SIGINT, handler)

    # 2. Get terminal dimensions
    cols, rows = shutil.get_terminal_size()
    
    colors = [
        '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m'
    ]
    reset = '\033[0m'
    shapes = ['*', '+', 'o', '.', '^', ',', 'v']

    # 3. Enter Alternate Screen Buffer & Hide Cursor
    # This ensures we don't overwrite your actual update logs
    print("\033[?1049h\033[?25l", end="", flush=True)

    particles = []
    
    # Animation Settings
    duration = 6.0        # Total animation time
    burst_time = 2.0      # How long the cannons keep firing
    start_time = time.time()
    
    # Physics Constants
    gravity = 0.15        # How fast they are pulled down
    drag = 0.92           # Air resistance (slows sideways movement)
    terminal_velocity = 1.0 # Max falling speed (so they float like paper, not rocks)

    try:
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # --- PHASE 1: FIRE CANNONS ---
            # Only spawn new particles during the "burst" phase
            if current_time - start_time < burst_time:
                for _ in range(5): # Spawn density per frame
                    
                    # LEFT CANNON (Bottom Left)
                    particles.append({
                        'x': 2.0,                  # Start at left edge
                        'y': float(rows),          # Start at bottom
                        'vx': random.uniform(1.0, 3.5),   # Shoot Right
                        'vy': random.uniform(-1.5, -4.0), # Shoot Up (Negative Y)
                        'char': random.choice(shapes),
                        'color': random.choice(colors)
                    })
                    
                    # RIGHT CANNON (Bottom Right)
                    particles.append({
                        'x': float(cols - 2),      # Start at right edge
                        'y': float(rows),          # Start at bottom
                        'vx': random.uniform(-1.0, -3.5), # Shoot Left
                        'vy': random.uniform(-1.5, -4.0), # Shoot Up
                        'char': random.choice(shapes),
                        'color': random.choice(colors)
                    })

            # --- PHASE 2: PHYSICS ENGINE ---
            buffer = ""
            alive_particles = []
            
            # Draw the Cannons at the bottom corners
            buffer += f"\033[{rows};1H{reset}◢" 
            buffer += f"\033[{rows};{cols}H{reset}◣"

            for p in particles:
                # 1. Clear old position (print space)
                old_scr_x = int(p['x'])
                old_scr_y = int(p['y'])
                if 1 <= old_scr_y <= rows and 1 <= old_scr_x <= cols:
                     buffer += f"\033[{old_scr_y};{old_scr_x}H "

                # 2. Update Physics
                p['x'] += p['vx']
                p['y'] += p['vy']
                
                p['vy'] += gravity           # Apply Gravity
                p['vx'] *= drag              # Apply Air Resistance

                # 3. Paper Flutter Effect
                # If particle is falling (vy > 0), add random sway
                if p['vy'] > 0:
                    if p['vy'] > terminal_velocity:
                        p['vy'] = terminal_velocity # Cap speed
                    p['vx'] += random.uniform(-0.1, 0.1) # Random sway

                # 4. Draw New Position
                scr_x = int(p['x'])
                scr_y = int(p['y'])
                
                # Only keep particle if it is above the floor
                if scr_y <= rows:
                    # Bounce off walls (optional, keeps confetti on screen)
                    if p['x'] <= 1:
                        p['x'] = 1
                        p['vx'] *= -0.6
                    elif p['x'] >= cols:
                        p['x'] = cols
                        p['vx'] *= -0.6
                    
                    # Draw
                    if 1 <= scr_y <= rows and 1 <= scr_x <= cols:
                        buffer += f"\033[{scr_y};{scr_x}H{p['color']}{p['char']}"
                        alive_particles.append(p)

            particles = alive_particles
            
            # Flush the entire frame at once
            print(buffer, end="", flush=True)
            time.sleep(0.04) # ~25 FPS

    except Exception:
        pass

    # 4. Cleanup (Restore screen)
    print("\033[?1049l\033[?25h", end="")

if __name__ == "__main__":
    confetti_cannons()
