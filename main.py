import os
import utils

if __name__ == "__main__":
    save_path = "results_dir"
    os.makedirs(save_path, exist_ok=True)
    utils.main('KAROL G', save_path)
