from .main import Server
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json

from tqdm import tqdm

if __name__ == "__main__":
    server = Server(__name__)
    app = server.app
    app.config.update({
        "TESTING": True,
    })

    app
    client = app.test_client()

    BENCHMARK = "E-n60-k5-s9.evrp"

    NB_GEN = 120

    bench_data = client.get(f"benchmark/{BENCHMARK}").json

    nodes = bench_data["NODES"]

    client.post("run", data={
        "type": "ga",
        "bench_id": BENCHMARK,
        "param": json.dumps({
            "nb_epochs": NB_GEN,
            "pop_size": 8,
            "mutation_rate": 0.1,
            "crossover_rate": 1
        })
    })


    fig = plt.figure()

    COLORS = [
        "b",
        "g",
        "r",
        "m",
        "y",
        "tab:brown",
        "tab:purple",
        "tab:grey"
    ]

    t = tqdm(total=NB_GEN - 1)

    points = [a for a in zip(*nodes.values())]

    xlim = (
        min(points[0])-10,
        max(points[0])+10
    )

    ylim = (
        min(points[1])-10,
        max(points[1])+10
    )

    def init():
        return plt.axes(xlim=xlim, ylim=ylim)

    def gen_fram(id):

        axis = plt.axes(xlim=xlim, ylim=ylim)

        generation = client.get("snapshot").json

        gen = generation["snapshot"]["individuals"][0]

        solution = gen["solution"]

        roads = []
        road = [solution[0]]
        for p in solution[1:]:
            road.append(p)
            if p == 0:
                roads.append(road)
                road = [p]

        roads_lines = []
        for road in roads:
            roads_lines.append(
                [a for a in zip(*[nodes[str(p)] for p in road])]
            )
    
        for i, road_lines in enumerate(roads_lines):
            axis.plot(*road_lines, COLORS[i], zorder=1)

        node_colors = ["k"] * len(nodes.values())
        for i in bench_data["STATIONS"]:
            node_colors[i] = "c"
    
        axis.scatter(*[a for a in zip(*nodes.values())], color=node_colors, zorder=2)

        fit = gen["fitness"]
    
        # txt = axis.set_title(f"Generation: {id}| {fit}")
        axis.text(0.05, 0.9, f"Generation: {id}| {fit}", transform=axis.transAxes)

        t.update()

        return axis

    anim = FuncAnimation(fig, gen_fram, init_func=init,
                         frames=NB_GEN-1, interval=500, repeat=False)

    # plt.show()
    anim.save("./vid/ECVRP.mp4", writer="ffmpeg")

    t.close()
