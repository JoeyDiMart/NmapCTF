import subprocess
import random
import os

# === CONFIG ===
REAL_INTERNAL_PORTS = [8080, 8081, 8082]
FAKE_INTERNAL_PORTS = [8888, 8889, 8890]
EXCLUDED_PORTS = set(REAL_INTERNAL_PORTS + FAKE_INTERNAL_PORTS + [8080])
PORT_RANGE = (1024, 49151)

def get_unique_random_ports(count, exclude):
    available = list(set(range(*PORT_RANGE)) - exclude)
    return random.sample(available, count)

# === STEP 1: Get random unique external ports ===
real_host_ports = get_unique_random_ports(3, EXCLUDED_PORTS)
EXCLUDED_PORTS.update(real_host_ports)

fake_host_ports = get_unique_random_ports(3, EXCLUDED_PORTS)
EXCLUDED_PORTS.update(fake_host_ports)

# === STEP 2: Build Docker image ===
print("[*] Building Docker image...")
subprocess.run(["docker", "build", "-t", "nmap-ctf", "."], check=True)

# === STEP 3: Stop old container ===
subprocess.run(["docker", "rm", "-f", "ctf-container"], stderr=subprocess.DEVNULL)

# === STEP 4: Build Docker run command with -p mappings ===
docker_cmd = ["docker", "run", "-d", "--name", "ctf-container"]
for hp, cp in zip(real_host_ports, REAL_INTERNAL_PORTS):
    docker_cmd += ["-p", f"{hp}:{cp}"]
for hp, cp in zip(fake_host_ports, FAKE_INTERNAL_PORTS):
    docker_cmd += ["-p", f"{hp}:{cp}"]
docker_cmd.append("nmap-ctf")

# === STEP 5: Run the container ===
print("[*] Starting Docker container...")
subprocess.run(docker_cmd, check=True)

# === STEP 6: Print port info ===
print("\n✅ CTF Challenge Started!")
print("🎯 Real Services:")
for i, (hp, cp) in enumerate(zip(real_host_ports, REAL_INTERNAL_PORTS), 1):
    print(f"  Host Port {hp} → Container Port {cp} (Challenge {i})")

print("\n🦴 Fake Services:")
for hp, cp in zip(fake_host_ports, FAKE_INTERNAL_PORTS):
    print(f"  Host Port {hp} → Container Port {cp} (Fake)")

print("\nPlayers can scan your IP to discover the correct ports.")
