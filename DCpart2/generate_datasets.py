import os
import random

# Fixed random seed for deterministic generation
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Output directory (always next to this file, wherever the script is run from)
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)

# Problem sizes for the 10 files (> 100, up to 2000)
SIZES = [120, 150, 200, 300, 500, 750, 1000, 1250, 1500, 2000]


def generate_closest_pair_files():
    """Generates 10 2D point set files with n > 100 points."""
    print("Generating Closest-Pair datasets...")
    for idx, n in enumerate(SIZES, start=1):
        filename = os.path.join(DATASET_DIR, f"cp_{idx:02d}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{n}\n")
            for _ in range(n):
                # Coordinates in range [-5000.0, 5000.0] with 4 decimal places
                x = round(random.uniform(-5000.0, 5000.0), 4)
                y = round(random.uniform(-5000.0, 5000.0), 4)
                f.write(f"{x} {y}\n")
        print(f"  Created {filename} (n = {n} points)")


def generate_integer_multiplication_files():
    """Generates 10 large integer multiplication files with digits > 100."""
    print("Generating Integer Multiplication datasets...")
    for idx, digits in enumerate(SIZES, start=1):
        filename = os.path.join(DATASET_DIR, f"mul_{idx:02d}.txt")
        # Ensure first digit is 1-9 to avoid leading zero issues
        first_x = str(random.randint(1, 9))
        rest_x = "".join(str(random.randint(0, 9)) for _ in range(digits - 1))
        x_str = first_x + rest_x

        first_y = str(random.randint(1, 9))
        rest_y = "".join(str(random.randint(0, 9)) for _ in range(digits - 1))
        y_str = first_y + rest_y

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{x_str}\n{y_str}\n")
        print(f"  Created {filename} (digits = {digits})")


def main():
    generate_closest_pair_files()
    generate_integer_multiplication_files()
    print("\nAll 20 datasets successfully created in 'datasets/'.")


if __name__ == "__main__":
    main()