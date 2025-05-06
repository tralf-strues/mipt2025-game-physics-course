import sympy as sp
import io
import plotly.graph_objects as go
from PIL import Image

def TaylorExpansionPolynomial(expression, functions, point, order, t):
    num_funcs = len(functions)

    replacing_symbols = [sp.symbols(f"{i}s") for i in range(num_funcs)]
    expansion = expression

    for i in range(num_funcs):
        expansion = expansion.replace(functions[i](t), replacing_symbols[i])

    for i in range(num_funcs):
        expansion = expansion.series(replacing_symbols[i], point[i], order).removeO()

    expansion = expansion.simplify()

    for i in range(num_funcs):
        expansion = expansion.replace(replacing_symbols[i], functions[i](t))

    return expansion.as_poly(*[func(t) for func in functions])

def SaveAnimationGif(fig, frames, fps, path, resolution=(500, 500), axis_ranges=[[0,6], [0,6]]):
    images = []
    print(f"Saving animation to '{path}' with {len(frames)} frames, {fps} fps, and resolution {resolution}...")
    for frame in frames:
        temp_fig = go.Figure(
            data=frame.data,
            layout=fig.layout
        )

        temp_fig.update_layout(
            xaxis=dict(range=axis_ranges[0], showgrid=False, zeroline=False),
            yaxis=dict(range=axis_ranges[1], showgrid=False, zeroline=False, scaleanchor='x', scaleratio=1),
            plot_bgcolor='white',
            width=resolution[0],
            height=resolution[1],
            margin=dict(l=0, r=0, t=0, b=0)
        )

        img_bytes = temp_fig.to_image(format="png")
        image = Image.open(io.BytesIO(img_bytes))
        images.append(image.convert("RGB"))

    images[0].save(path, save_all=True, append_images=images[1:], duration=1000/fps, loop=0)
    print(f"Successfully saved animation to '{path}'")