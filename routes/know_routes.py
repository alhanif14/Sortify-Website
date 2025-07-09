from fasthtml.common import *
from function.know import know_section

def know_routes(rt):
    @rt("/know")
    def know():
        return know_section()