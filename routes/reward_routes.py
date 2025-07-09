from fasthtml.common import *
from function.reward import reward_section

def reward_routes(rt):
    @rt("/reward")
    def reward():
        return reward_section()