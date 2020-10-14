
from flask import Flask, render_template
from threading import Thread
from flask import jsonify
import json
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask('')


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    fig.patch.set_facecolor('#212121')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    text_file = open("datalist.txt", "r")
    lines = text_file.read().split(',')
    lines = [int(i) for i in lines]
    print(lines)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(36)
    ys = lines
    # axis.xlabel(" ")
    # axis.ylabel("mg/dL")
    axis.axis(ymin=40, ymax=400)
    axis.spines['bottom'].set_color('#FFFFFF')
    axis.spines['top'].set_color('#FFFFFF')
    axis.spines['right'].set_color('#FFFFFF')
    axis.spines['left'].set_color('#FFFFFF')

    axis.tick_params(axis='x', colors='#FFFFFF')
    axis.tick_params(axis='y', colors='#FFFFFF')

    axis.yaxis.label.set_color('#FFFFFF')
    axis.xaxis.label.set_color('#FFFFFF')
    axis.set_facecolor("#212121")
    axis.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
    axis.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        labelsize=16)
    axis.scatter(xs, ys, s=50, color="#eb349e")
    axis.set_axisbelow(True)
    axis.grid(b=True, which="both", axis="y", linewidth=1)

    return fig


@app.route('/plot2.png')
def plot_png2():
    fig = create_figure2()
    fig.patch.set_facecolor('#212121')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure2():
    text_file = open("datalist.txt", "r")
    lines = text_file.read().split(',')
    lines = [int(i) for i in lines]
    print(lines)
    fig = Figure(figsize=(40, 15))
    axis = fig.add_subplot(1, 1, 1)
    xs = range(36)
    ys = lines
    # axis.xlabel(" ")
    # axis.ylabel("mg/dL")
    axis.axis(ymin=40, ymax=350)
    axis.spines['bottom'].set_color('#FFFFFF')
    axis.spines['top'].set_color('#FFFFFF')
    axis.spines['right'].set_color('#FFFFFF')
    axis.spines['left'].set_color('#FFFFFF')

    axis.tick_params(axis='x', colors='#FFFFFF')
    axis.tick_params(axis='y', colors='#FFFFFF')

    axis.yaxis.label.set_color('#FFFFFF')
    axis.xaxis.label.set_color('#FFFFFF')
    axis.set_facecolor("#212121")
    axis.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
    axis.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        labelsize=50)
    axis.set_axisbelow(True)
    axis.grid(b=True, which="both", axis="y", linewidth=2.5)
    axis.scatter(xs, ys, s=1500, color="#eb349e")
    axis.set_yscale("linear")
    return fig


@app.route("/img")
def img():
    return render_template("img.html")


@app.route('/')
def home():
    f = open("output.txt", "r")
    data = json.loads(f.read())
    return jsonify(data)


def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except:  # noqa: E722
        pass


def keep_alive():
    t = Thread(target=run)
    t.start()
