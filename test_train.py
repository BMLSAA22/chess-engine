"""Quick test to verify the training pipeline works."""
from train import create_fresh_board, generate_trajectory
from model import Net

print("Imports OK")
net = Net()
print("Model created")
lp, r, result = generate_trajectory(net, max_t=5)
print(f"Trajectory OK: {len(lp)} steps, result={result}")
print(f"Rewards: {r}")
print("\nEverything works! You can now run: python train.py")
