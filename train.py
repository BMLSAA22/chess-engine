"""
Train a chess agent using REINFORCE (Policy Gradient).

The agent (White) learns to play chess by:
- Using a CNN policy network to select moves
- Playing against a heuristic opponent (Black) that captures when possible
- Receiving rewards for captures, promotions, checkmate, and penalties for losing

Usage:
    python train.py
"""

import torch
import torch.optim as optim
import numpy as np
import copy
import os
from collections import deque

from board import board as init_board
from piece import piece
from agent import agent
from model import Net


# ============================================================
# HYPERPARAMETERS
# ============================================================
NUM_EPISODES = 500        # Total training games
MAX_MOVES = 100           # Max moves per game
LEARNING_RATE = 1e-3      # Optimizer learning rate
GAMMA = 0.99              # Discount factor for future rewards
PRINT_EVERY = 10          # Print stats every N episodes
SAVE_EVERY = 50           # Save model checkpoint every N episodes
CHECKPOINT_DIR = "checkpoints"

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_fresh_board():
    """Create a fresh board state for a new game."""
    fresh_board = {}
    for i in range(1, 9):
        for j in range(1, 9):
            fresh_board[(i, j)] = ''

    for i in range(1, 9):
        fresh_board[(2, i)] = piece(piece="P", color="W", moved=False, position=(2, i), tag="WP" + str(i))
        fresh_board[(7, i)] = piece(piece="P", color="B", moved=False, position=(7, i), tag="BP" + str(i))

    fresh_board[(1, 1)] = piece(piece="R", color="W", moved=False, position=(1, 1), tag="WR1")
    fresh_board[(8, 1)] = piece(piece="R", color="B", moved=False, position=(8, 1), tag="BR1")
    fresh_board[(1, 2)] = piece(piece="N", color="W", moved=False, position=(1, 2), tag="WN1")
    fresh_board[(8, 2)] = piece(piece="N", color="B", moved=False, position=(8, 2), tag="BN1")
    fresh_board[(1, 3)] = piece(piece="B", color="W", moved=False, position=(1, 3), tag="WB1")
    fresh_board[(8, 3)] = piece(piece="B", color="B", moved=False, position=(8, 3), tag="BB1")
    fresh_board[(1, 4)] = piece(piece="Q", color="W", moved=False, position=(1, 4), tag="WQ")
    fresh_board[(8, 4)] = piece(piece="Q", color="B", moved=False, position=(8, 4), tag="BQ")
    fresh_board[(1, 5)] = piece(piece="K", color="W", moved=False, position=(1, 5), tag="WK")
    fresh_board[(8, 5)] = piece(piece="K", color="B", moved=False, position=(8, 5), tag="BK")
    fresh_board[(1, 6)] = piece(piece="B", color="W", moved=False, position=(1, 6), tag="WB2")
    fresh_board[(8, 6)] = piece(piece="B", color="B", moved=False, position=(8, 6), tag="BB2")
    fresh_board[(1, 7)] = piece(piece="N", color="W", moved=False, position=(1, 7), tag="WN2")
    fresh_board[(8, 7)] = piece(piece="N", color="B", moved=False, position=(8, 7), tag="BN2")
    fresh_board[(1, 8)] = piece(piece="R", color="W", moved=False, position=(1, 8), tag="WR2")
    fresh_board[(8, 8)] = piece(piece="R", color="B", moved=False, position=(8, 8), tag="BR2")

    return fresh_board


def discount_rewards(rewards, gamma=GAMMA):
    """Compute discounted rewards (returns) for REINFORCE."""
    discounted = np.zeros(len(rewards))
    running_sum = 0
    for t in reversed(range(len(rewards))):
        running_sum = running_sum * gamma + rewards[t]
        discounted[t] = running_sum
    # Normalize for stable training
    if len(discounted) > 1:
        discounted = (discounted - discounted.mean()) / (discounted.std() + 1e-9)
    return discounted


def generate_trajectory(policy_net, max_t=MAX_MOVES):
    """
    Play one full game:
      - White uses the policy network
      - Black uses a heuristic (captures high-value pieces when possible)
    
    Returns:
      - saved_log_probs: log probabilities of White's actions
      - rewards: reward at each timestep
      - game_result: "white_wins", "black_wins", "stalemate", or "max_moves"
    """
    # Fresh game
    board = create_fresh_board()
    game_agent = agent(board)

    saved_log_probs = []
    rewards = []
    game_result = "max_moves"

    for t in range(max_t):
        # --- WHITE's turn (policy network) ---
        state = game_agent.board_to_array()
        mask, mp = game_agent.rel_to_abs_moves()

        # Check if mask has any legal moves
        if mask.sum() == 0:
            # No legal moves for white
            if game_agent.isCheck("W"):
                game_result = "black_wins"
                rewards.append(-50.0)
            else:
                game_result = "stalemate"
                rewards.append(-5.0)
            break

        action_id, log_prob = policy_net.sample(state, mask)
        action = mp[action_id]

        white_reward = game_agent.make_move(action['tag'], action['to'], action['castles'])

        # Check game state after white's move
        if game_agent.checkmate("B"):
            game_result = "white_wins"
            saved_log_probs.append(log_prob)
            rewards.append(100.0)
            break

        if game_agent.stalemate("B"):
            game_result = "stalemate"
            saved_log_probs.append(log_prob)
            rewards.append(-5.0)
            break

        # --- BLACK's turn (heuristic opponent) ---
        black_moves = game_agent.possible_moves("B")
        if len(black_moves) == 0:
            if game_agent.isCheck("B"):
                game_result = "white_wins"
                saved_log_probs.append(log_prob)
                rewards.append(100.0)
            else:
                game_result = "stalemate"
                saved_log_probs.append(log_prob)
                rewards.append(-5.0)
            break

        tag, to, castles = game_agent.sample("B")
        black_reward = game_agent.make_move(tag, to, castles)

        # Check game state after black's move
        if game_agent.checkmate("W"):
            game_result = "black_wins"
            saved_log_probs.append(log_prob)
            rewards.append(-50.0)
            break

        if game_agent.stalemate("W"):
            game_result = "stalemate"
            saved_log_probs.append(log_prob)
            rewards.append(-5.0)
            break

        # Step reward: difference between white and black rewards
        step_reward = white_reward - black_reward
        saved_log_probs.append(log_prob)
        rewards.append(step_reward)

    return saved_log_probs, rewards, game_result


# ============================================================
# TRAINING LOOP
# ============================================================

def train():
    """Main training loop using REINFORCE."""
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize policy network and optimizer
    policy_net = Net().to(device)
    optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)

    # Create checkpoint directory
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    # Tracking
    scores_window = deque(maxlen=50)
    all_rewards = []
    wins = 0
    losses = 0
    draws = 0

    print("=" * 60)
    print("Starting REINFORCE Training")
    print(f"Episodes: {NUM_EPISODES} | Max moves: {MAX_MOVES}")
    print(f"LR: {LEARNING_RATE} | Gamma: {GAMMA}")
    print("=" * 60)

    for episode in range(1, NUM_EPISODES + 1):
        # Generate a game trajectory
        log_probs, rewards, result = generate_trajectory(policy_net, MAX_MOVES)

        # Track results
        total_reward = sum(rewards)
        scores_window.append(total_reward)
        all_rewards.append(total_reward)

        if result == "white_wins":
            wins += 1
        elif result == "black_wins":
            losses += 1
        else:
            draws += 1

        # Compute policy gradient loss
        if len(log_probs) > 0 and len(rewards) > 0:
            discounted = discount_rewards(rewards)
            policy_loss = []

            for log_prob, G in zip(log_probs, discounted):
                policy_loss.append(-log_prob * G)

            # Backpropagation
            optimizer.zero_grad()
            policy_loss = torch.stack(policy_loss).sum()
            policy_loss.backward()
            torch.nn.utils.clip_grad_norm_(policy_net.parameters(), max_norm=1.0)
            optimizer.step()

        # Logging
        if episode % PRINT_EVERY == 0:
            avg_reward = np.mean(scores_window)
            win_rate = wins / episode * 100
            print(
                f"Episode {episode:4d} | "
                f"Avg Reward: {avg_reward:7.2f} | "
                f"Last Result: {result:12s} | "
                f"Win Rate: {win_rate:5.1f}% | "
                f"W/L/D: {wins}/{losses}/{draws}"
            )

        # Save checkpoint
        if episode % SAVE_EVERY == 0:
            checkpoint_path = os.path.join(CHECKPOINT_DIR, f"policy_net_ep{episode}.pth")
            torch.save({
                'episode': episode,
                'model_state_dict': policy_net.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'avg_reward': np.mean(scores_window),
                'wins': wins,
                'losses': losses,
                'draws': draws,
            }, checkpoint_path)
            print(f"  -> Saved checkpoint: {checkpoint_path}")

    # Final save
    final_path = os.path.join(CHECKPOINT_DIR, "policy_net_final.pth")
    torch.save(policy_net.state_dict(), final_path)
    print(f"\nTraining complete! Final model saved to: {final_path}")
    print(f"Final stats: W/L/D = {wins}/{losses}/{draws} | Win rate: {wins/NUM_EPISODES*100:.1f}%")

    return policy_net, all_rewards


if __name__ == "__main__":
    policy_net, rewards = train()
