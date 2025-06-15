from mpi4py import MPI
import time
import random
from vehicle_simulation import update_intersection_traffic
from ai_module import predict_congestion
from ml_module import predict_green_direction
from utils import logical_clock  # Optional: keep for snapshots

import pygame
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

clock = 0
node_data = {}

if rank == 0:
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Decentralized Traffic Dashboard")
    font = pygame.font.SysFont("Arial", 18)
    running = True

    while running:
        screen.fill((30, 30, 30))

        for i in range(1, size):
            if comm.Iprobe(source=i, tag=42):
                node_data[i] = comm.recv(source=i, tag=42)

        for i, data in node_data.items():
            base_x = 50 + ((i - 1) * 230)
            base_y = 100
            pygame.draw.rect(screen, (50, 50, 50), (base_x, base_y, 200, 200), 2)

            y_offset = 0
            for d in ['North', 'East', 'South', 'West']:
                txt = f"{d}: {len(data['traffic'][d])} [{'P' if 'priority' in data['traffic'][d] else ''}]"
                t = font.render(txt, True, (255, 255, 255))
                screen.blit(t, (base_x + 10, base_y + 10 + y_offset))
                y_offset += 25

            t2 = font.render(f"Green: {data['green_dir']} | Clock: {data['clock']}", True, (0, 255, 0))
            t3 = font.render(f"Congestion: {data['congestion']}", True, (255, 255, 0))
            screen.blit(t2, (base_x + 10, base_y + 120))
            screen.blit(t3, (base_x + 10, base_y + 150))
            t4 = font.render(f"Node {i}", True, (0, 200, 255))
            screen.blit(t4, (base_x + 10, base_y - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

else:
    # Initial state
    intersection_traffic = update_intersection_traffic()
    green_dir = predict_green_direction(intersection_traffic)

    while True:
        intersection_traffic = update_intersection_traffic(intersection_traffic, green_dir)
        clock = logical_clock(clock)

        # ML-based green light decision
        green_dir = predict_green_direction(intersection_traffic)

        # Build status
        vehicle_counts = {d: len(q) for d, q in intersection_traffic.items()}
        priorities = [d for d in intersection_traffic if 'priority' in intersection_traffic[d]]
        congestion = predict_congestion(sum(vehicle_counts.values()))

        status = {
            'rank': rank,
            'green_dir': green_dir,
            'clock': clock,
            'vehicle_counts': vehicle_counts,
            'priority_dirs': priorities,
            'congestion': congestion,
            'traffic': intersection_traffic
        }

        # Optional: snapshot trigger
        if random.random() < 0.05:
            pass  # Replace this with initiate_snapshot(...) if using snapshots

        comm.send(status, dest=0, tag=42)
        time.sleep(2)
