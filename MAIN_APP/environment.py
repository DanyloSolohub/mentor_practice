import os

import environ


current_path = environ.Path(__file__)
site_root = current_path - 2

env = environ.Env()

environ.Env.read_env(env_file=os.path.join(site_root, '.env'))