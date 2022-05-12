import argparse
import logging
import os
from server import app

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--debug", action=argparse.BooleanOptionalAction)
    debug = args.parse_args().debug
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG,
                        )
    app.run("0.0.0.0", port=os.getenv("PORT", 8000), debug=debug)
