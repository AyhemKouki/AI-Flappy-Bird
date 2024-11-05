# Flappy Bird NEAT AI


Uploading Untitled video - Made with Clipchamp (3).mp4…

This project is a Python implementation of Flappy Bird powered by the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The objective is for the AI, using neural networks evolved through NEAT, to learn how to play the game by controlling the bird's movements, navigating through pipes, and maximizing its fitness score.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How NEAT is Used](#how-neat-is-used)

---


## Features
- **Bird Animation:** The bird has a flapping animation for a realistic visual.
- **Pipe Movement:** Randomly spawned pipes with set gaps that scroll from right to left.
- **Scrolling Background and Base:** The background and base continuously scroll to simulate forward movement.
- **Score Tracking:** Displays the current score in the top-left corner.
- **NEAT Integration:** Utilizes the NEAT algorithm to evolve neural networks that control the bird’s behavior.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AyhemKouki/AI-Flappy-Bird.git
    cd flappy-bird-neat
    ```

2. Ensure you have the images in the `imgs` folder:
    - `bird1.png`, `bird2.png`, `bird3.png` - Frames of the bird's animation.
    - `pipe.png` - Image for the pipes.
    - `bg.png` - Background image.
    - `base.png` - Base image.

3. Configure NEAT parameters:
   - Modify `config.txt` for NEAT settings (population size, mutation rates, etc.).

## Usage
To run the game and start training the AI:
  ```bash
  python flappy_bird_neat.py
  ```
## How NEAT is Used
  Each bird is controlled by a neural network that makes a decision (to flap or not) based on the bird's current state:
  - Bird's Y position
  - Bird's Y velocity
  - Distance to the next pipe
  - Gap above and below the bird.
