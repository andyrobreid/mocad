import marimo

__generated_with = "0.17.5"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import build123d as bd
    import typer as typ
    return bd, mo, typ


@app.cell
def _(mo):
    sld_width = mo.ui.slider(label="Width", start=1, step=0.5, stop=10, value=10)
    sld_height = mo.ui.slider(label="Height", start=1, step=0.1, stop=10, value=10)
    sld_length = mo.ui.slider(label="Length", start=1, step=0.1, stop=10, value=10)
    return sld_height, sld_length, sld_width


@app.cell
def _(bd, mo, typ):
    app = typ.Typer(help="Cli | Notebook example to build models with codecad")


    def build_box(height=10, length=10, width=10, wall=1):
        """
        With provided input, build the box
        """
        with bd.BuildPart() as box:
            bd.Box(height=length, length=width, width=height)
            r = (min(length, width) - wall) / 2

            print(dict(length=length, height=height, width=width, radius=r))
            bd.Cylinder(
                height=height,
                radius=r,
                rotation=(90, 0, 0),
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX),
                mode=bd.Mode.SUBTRACT,
            )

        return box


    @app.command()
    def volume(height=10, length=10, width=10, wall=1):
        """
        Get the volume of the box part built from provided inputs
        """

        box = build_box(height, length, width, wall)

        volume = round(box.part.volume, 2)

        if mo.app_meta().mode == "script":
            print(volume)
        return volume


    @app.command()
    def export(
        height: float = 10.0,
        length: float = 10.0,
        width: float = 10.0,
        wall: float = 1,
        type: str = "stl",
        name: str = "box",
        output_dir: str = "./tmp/",
    ):
        """
        Export the box part built from provided inputs
        """
        _box = build_box(height, length, width)
        match type:
            case "stl":
                path = f"{output_dir}{name}.stl"
                bd.export_stl(to_export=_box.part, file_path=path)
                print(f"Exported {path}")
            case "gltf":
                path = f"{output_dir}{name}.gltf"
                bd.export_gltf(to_export=_box.part, file_path=path)
                print(f"Exported {path}")
            case _:
                print(
                    f"`{type}` is currently not supported. Try `stl`, `gltf` instead"
                )
    return app, build_box, volume


@app.cell
def _(mo, sld_height, sld_length, sld_width):
    mo.vstack([sld_width, sld_height, sld_length])
    return


@app.cell
def _(build_box, mo, sld_height, sld_length, sld_width, volume):
    # I only want this cell to run in edit mode, outputs a viewer of the part
    mo.stop(predicate=mo.app_meta().mode != "edit")

    inputs = dict(
        height=sld_height.value, length=sld_length.value, width=sld_width.value
    )

    mo.vstack([build_box(**inputs).part, volume(**inputs)])
    return


@app.cell
def _(app, mo):
    # Run the cli application
    if mo.app_meta().mode == "script":
        app()
    return


if __name__ == "__main__":
    app.run()
