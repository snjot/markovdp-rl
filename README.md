# markovdp-rl

This is the implementation of reinforcement learning algorithm for Markov Decision Process environment, greatly owed to [baby-steps-of-rl-ja](https://github.com/icoxfog417/baby-steps-of-rl-ja).

![Markov DP RL Image](./doc/markovdp-rl.png)

## How to Play

```zsh
git clone git@github.com:snjot/markovdp-rl.git
cd markovdp-rl
poetry run python -m markovdp --gui --delay 0.2
```

### Play with Smart Agents

You can play with smart agents as follows:

```zsh
poetry run python -m markovdp --gui --delay 0.2 --method PolicyIter
```

Available methods:

| argument              | method the agent applies  |
| --------------------- | ------------------------- |
| `--method PolicyIter` | Policy Iteration          |
| `--method ValueIter`  | Value Iteration           |
| None of the above     | Random Action (No Policy) |

## Improvement

- add type hint
- separate code into files
- improve design
- make State immutable
- add verbose mode
- add GUI mode

## Implemented

- [x] PolicyIteration
- [x] ValueIteration

## TODO

- [ ] implement Monte Carlo agent
