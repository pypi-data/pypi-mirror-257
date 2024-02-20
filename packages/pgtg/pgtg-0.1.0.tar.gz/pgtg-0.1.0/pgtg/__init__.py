from gymnasium.envs.registration import register

from pgtg.environment import PGTGEnv

__version__ = "0.1.0"

register(id="pgtg-v0", entry_point="pgtg.environment:PGTGEnv")
