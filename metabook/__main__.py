"""
Entry point to create app.
@author: iXB3 (Matteo Causio)
"""

# # Package # #
from metabook.app import create, run


if __name__ == '__main__':
    """Entry point: run app"""
    run(app=create())