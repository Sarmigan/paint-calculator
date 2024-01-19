import math

# IMPLEMENT SORTING SIZE/PRICE
class PaintBrand:
    def __init__(self, name, sizes, prices):
        self.name = name
        self.sizes = sizes
        self.prices = prices

def get_measurement(question, max, min):
    val = ""
    val = float(input(question))
    if val < 0:
        val = get_measurement(f"Please enter a measurement above zero (metres):\n", max, min)
    elif val < min:
        val = get_measurement(f"Please enter a measurement above {min} (metres):\n", max, min)
    elif val > max:
        val = get_measurement(f"Please enter a measurement below {max} (metres):\n", max, min)

    return val

def get_choice(question, choices):
    choice = ""
    choice = input(question)
    while choice not in choices:
        choice = input(f"Choose one of {choices}:\n")
    return choice

def calculate_total_price(val, sizes, prices):
    sizes.reverse()
    prices.reverse()

    total = [0, sizes, [0] * len(sizes)]
    target = val

    curr_size_index = 0
    while target>0:
        if(target < sizes[curr_size_index] and curr_size_index < (len(sizes)-1)):
            price_diff_next_size_target = abs(target - sizes[curr_size_index+1]) * (prices[curr_size_index+1]/sizes[curr_size_index+1]) # Calculates cost difference between target and next size using price per litre of size
            price_diff_curr_size_target = abs(target - sizes[curr_size_index]) * (prices[curr_size_index]/sizes[curr_size_index]) # Calculates cost difference between target and current size using price per litre of size
            if(price_diff_next_size_target < price_diff_curr_size_target):
                curr_size_index += 1

        total[2][curr_size_index] += 1
        target -= sizes[curr_size_index]
        total[0] += prices[curr_size_index]

    return total

if __name__ == "__main__":
    MAX_WALLS = 10
    MAX_DOORS = 6
    MAX_WINDOW = 6
    PAINT_PSQM = 0.1

    good_home = PaintBrand("GoodHome", [0.05, 2.5, 5], [2.25, 16, 22])
    dulux = PaintBrand("Dulux", [0.03, 2.5, 5], [2.45, 22, 34])
    crown = PaintBrand("Crown", [0.04, 2.5, 5], [7.89, 25, 40])

    paints = [good_home, dulux, crown]

    while(True):
        paint_totals = []

        walls = int(get_choice("How many walls will you be painting?\n", [f"{i}" for i in range(1, MAX_WALLS+1)]))
        
        for wall in range(walls):
            unpainted_areas = []

            wall_length =  get_measurement(f"What is the length of wall {wall+1} (metres)?\n", 100, 0)
            wall_width = get_measurement(f"What is the width of wall {wall+1} (metres)?\n", 100, 0)
            
            doors = int(get_choice("How many doors does the wall have?\n", [f"{i}" for i in range(0, MAX_DOORS+1)]))

            for door in range(doors):
                door_length = get_measurement(f"What is the length of door {door+1} (metres)?\n", wall_length, 0)
                door_width = get_measurement(f"What is the width of door {door+1} (metres)?\n", wall_width, 0)

                unpainted_areas.append(door_length * door_width)

            windows = int(get_choice("How many windows does the wall have?\n", [f"{i}" for i in range(0, MAX_WINDOW+1)]))

            for window in range(windows):
                window_shape = int(get_choice(f"What shape is window {window+1}? (0 - rectangle/square, 1 - circle, 2 - triangle)\n", [f"{i}" for i in range(0, 3)]))

                match window_shape:
                    case 0:
                        window_length = get_measurement(f"What is the length of window {window+1} (metres)?\n", wall_length, 0)
                        window_width = get_measurement(f"What is the width of window {window+1} (metres)?\n", wall_width, 0)
                        unpainted_areas.append(window_length * window_width)                        
                    case 1:
                        window_diameter = get_measurement(f"What is the diameter of window {window+1} (metres)?\n", min(wall_length, wall_width), 0)
                        unpainted_areas.append(math.pi * math.pow((window_diameter/2), 2))
                    case 2:
                        window_length = get_measurement(f"What is the length of window {window+1} (metres)?\n", wall_length, 0)
                        window_width = get_measurement(f"What is the width of window {window+1} (metres)?\n", wall_width, 0)
                        unpainted_areas.append((window_length * window_width)/2)
                    case _:
                        pass

            coats = int(get_choice(f"How many coats of paint will you be applying to wall {wall + 1}?\n", [f"{i}" for i in range(1, 4)]))
            
            area = (wall_length * wall_width) - sum(unpainted_areas)
            paint_totals.append(PAINT_PSQM * area * coats)

        for i, paint in enumerate(paints):
            print(f"\n{i} - {paint.name}\n")
            for price, size in zip(paint.prices, paint.sizes):
                print(f"\t{size}L - £{price}")
        
        brand_choice = int(get_choice("\nPlease choose a paint brand:\n", [f"{i}" for i in range(0, 3)]))

        totals = calculate_total_price(sum(paint_totals), paints[brand_choice].sizes, paints[brand_choice].prices)
            
        print("\n###########################################")
        for i, total in enumerate(paint_totals):
            print(f"You need {total} litres of paint for wall {i+1}\n")
        print(f"\nYou need {sum(paint_totals)} litres of paint in total\n")
        print(f"\nBuying {paints[brand_choice].name} paint will cost you £{totals[0]}\n")
        for i,size in enumerate(totals[1]):
            if totals[2][i] != 0:
                print(f"You need {totals[2][i]} {size}L can/s of {paints[brand_choice].name} paint")
            
        print("###########################################")

        input("\nPress enter to calculate new paint")