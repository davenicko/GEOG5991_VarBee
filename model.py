#!/usr/bin/env python3
# model.py - The driver for the VarBee model

# Set environment

# Place hives

# Place flowers

# Place bees in hives

# Place mites

import varbee

bee = varbee.Bee()

for i in range(100):
    print("position number ", i, bee.get_position())
    bee.random_move()
