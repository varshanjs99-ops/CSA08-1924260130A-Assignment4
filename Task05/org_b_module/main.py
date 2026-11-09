from pathlib import Path
import attendance

if __name__ == "__main__":
    root = Path(__file__).parent
    print(attendance.run(root/"../data/attendance.csv", root/"output"))
