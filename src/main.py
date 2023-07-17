from environment import EdenEnvironment
from plant import SimplePlant


def create_report(env, plant):
    return f"<<Report>>\n{str(env)}\n{str(plant)}"

def main():
    env = EdenEnvironment()
    plant = SimplePlant(env)

    time = 0
    hours = 24 * 1
    dead = False

    for _ in range(hours):
        print(create_report(env, plant))
        print("*" * 80)

        for _ in range(60 * 60):
            time += 1
            plant.store_stats()

            env.pass_time()
            plant.pass_time()

            if dead := not plant.alive():
                print("!" * 80)
                print("Plant Died")
                print("!" * 80)
                break

        if dead:
            break

    print(create_report(env, plant))

    # time = list(range(plant.age))
    # temp = list(map(env.temperature_func, time))
    # moisture = list(map(env.moisture_func, time, temp))
    # light = list(map(env.light_func, time))

    _, axs = plt.subplots(4, len(plant.components))

    for i, comp in enumerate(plant.components):
        time = list(range(comp.age))
        for j, stat in enumerate(comp.stats):
            axs[j, i].plot(time, comp.stats[stat])
            axs[j, i].set_title(f"{comp.name} {stat}")

    plt.show()

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    main()

