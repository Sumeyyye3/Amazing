import random
from typing import Dict, List, Optional, Tuple

from kruskal import generate_kruskal_maze
from print_maze import write_maze_txt

def create_maze(config: Dict) -> List[List[Dict[str, bool]]]:
    """Rastgele yeni bir seed ile yeni bir labirent üretir."""
    new_seed = random.randint(0, 10**9)
    return generate_kruskal_maze(config["WIDTH"], config["HEIGHT"], new_seed)


def menu(config: Dict, cells: List[List[Dict[str, bool]]], shortest_path: str) -> None:
    """a_maze_ing.py'nin main() fonksiyonu ilk çizimi yaptıktan sonra

    kontrolü buraya devreder. `shortest_path`, a_maze_ing.py'de hesaplanıp
    buraya aktarılır: arkadaşın en kısa yol algoritmasını yazınca, sadece
    a_maze_ing.py'deki değeri değiştirmesi yeterli olacak, burada hiçbir
    şey değişmeyecek.
    """
    entry = config["ENTRY"]
    exit_ = config["EXIT"]
    color_index = 0
    show_path = False

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            cells = create_maze(config)
            show_path = False
        elif choice == "2":
            show_path = True
        elif choice == "3":
            ...  #renkler oluşturulacak
        elif choice == "4":
            print("Byy byy <3!")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 4.")
            continue

        write_maze_txt(cells, config["OUTPUT_FILE"], entry, exit_, shortest_path)
