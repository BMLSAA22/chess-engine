# Chess Engine with Reinforcement Learning

A chess engine built from scratch in Python, trained using policy gradient methods (Actor-Critic) with PyTorch.

## Overview

This project implements:
- A complete chess game engine with custom board representation
- Legal move generation with check/checkmate/stalemate detection
- A CNN-based policy network for move selection
- Training via policy gradient / actor-critic methods

## Architecture

```
├── agent.py          # Game logic: move execution, check detection, legal moves
├── board.py          # Board initialization (starting position)
├── piece.py          # Piece class with movement rules
├── moves.py          # Move generation helpers (diagonal, rook, knight, king)
├── model.py          # PyTorch CNN policy network
├── main.py           # Training loop and trajectory generation
├── utils/
│   ├── decode_FEN.py       # FEN notation parser
│   ├── model_env_map.py    # Action space mapping (index → move)
│   └── one_hot_encode.py   # Piece encoding utilities
└── notebooks/
    ├── actor-critic.ipynb
    ├── actor-critic_2.ipynb
    └── predicting_evaluation.ipynb
```

## How It Works

### Board Representation
The board is an 8×8 grid stored as a dictionary mapping `(row, col)` tuples to piece objects. The neural network sees the board as a `6×8×8` tensor (6 piece types, with +1 for white and -1 for black).

### Move Generation
Each piece type has its own move generation logic. Legal moves are filtered by checking if the resulting position leaves the king in check (using deep copies of the board state).

### Neural Network
- **Input**: 6×8×8 board tensor (one channel per piece type)
- **Architecture**: 3-layer CNN with max pooling → fully connected layers
- **Output**: Probability distribution over all possible moves (masked by legal moves)

### Training
The model is trained using REINFORCE (policy gradient):
- White plays using the neural network policy
- Black plays using a heuristic (captures high-value pieces when possible)
- Rewards are based on material advantage (captures, promotions, checkmate)

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Requirements

- Python 3.8+
- PyTorch 2.0+
- NumPy
- Matplotlib (for board visualization)

## Status

🚧 **Work in Progress** — The chess engine core is functional. The RL training pipeline is under active development.

## Future Plans

- [ ] Complete actor-critic training loop
- [ ] Add en passant
- [ ] Self-play training
- [ ] Integration with Stockfish for evaluation
- [ ] Opening book
- [ ] Model checkpointing and evaluation metrics
