import marimo

__generated_with = "0.17.5"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import build123d as bd
    import typer as typ
    import pathlib as pt
    import pickle as pk
    import base64
    import inspect


    __version__ = "1.0.0"
    return __version__, base64, bd, mo, pk, pt, typ


@app.cell
def _(__version__, base64, bd, pk, pt, typ):
    app = typ.Typer(help="Cli | Notebook example to build models with codecad")

    app.command()

    # TODO utilise tuple as input for the input parameters, order matters


    def export(obj: bd.BuildPart, fp: pt.Path):
        """
        Export the box part built from provided inputs
        """
        typ = fp.suffix
        match typ:
            case ".stl":
                bd.export_stl(to_export=obj.part, file_path=fp)
                print(f"Exported {fp}")
            case ".gltf":
                bd.export_gltf(to_export=obj.part, file_path=fp)
                print(f"Exported {fp}")
            case _:
                print(
                    f"`{typ}` is currently not supported. Try `stl`, `gltf` instead"
                )


    @app.command()
    def generate(
        height: float = 10,
        length: float = 10,
        width: float = 10,
        wall: float = 1,
        volume: bool = False,
        fp: str = None,
    ):
        """
        With provided input, cli entry point
        """
        with bd.BuildPart() as box:
            bd.Box(height=length, length=width, width=height)
            r = (min(length, width) - wall) / 2

            bd.Cylinder(
                height=height,
                radius=r,
                rotation=(90, 0, 0),
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX),
                mode=bd.Mode.SUBTRACT,
            )

        output = dict(
            obj=box,
            param=dict(
                length=length,
                height=height,
                width=width,
                wall=wall,
                version=__version__,
            ),
            results=dict(
                radius=r,
            ),
        )
        output["param"]["code"] = base64.b64encode(
            pk.dumps(obj=output.get("param"))
        )
        print(f"""
        Generated part with params:

        {output["param"]}

        with results:

        {output["results"]}
        """)

        if volume:
            volume = round(box.part.volume, 2)
            print(volume)

        if fp:
            path = pt.Path(fp)
            export(obj=output["obj"], fp=path)

        return output
    return app, generate


@app.cell
def _(mo):
    sld_width = mo.ui.slider(label="Width", start=1, step=0.5, stop=10, value=10)
    sld_height = mo.ui.slider(label="Height", start=1, step=0.1, stop=10, value=10)
    sld_length = mo.ui.slider(label="Length", start=1, step=0.1, stop=10, value=10)
    num_wall = mo.ui.number(label="Wall", value=1)
    num_density = mo.ui.number(label="Density")
    return num_wall, sld_height, sld_length, sld_width


@app.cell(hide_code=True)
def _(build, mo, num_wall, sld_height, sld_length, sld_width):
    vol2dp = round(build["obj"].part.volume, 2)
    den_pla_gccm = 1.24
    mass = round(den_pla_gccm * vol2dp / 1000, 2)

    md_mass = mo.md(f"""
    With a volume of {vol2dp} mm^3, density of {den_pla_gccm} grams per cubic centimeter, the mass calculates to {mass} grams.
    """)

    mo.vstack([sld_width, sld_height, sld_length, num_wall, md_mass])
    return


@app.cell(hide_code=True)
def _(base64, generate, mo, num_wall, pk, sld_height, sld_length, sld_width):
    # I only want this cell to run in edit mode, outputs a viewer of the part
    mo.stop(predicate=mo.app_meta().mode != "edit")

    build = generate(
        height=sld_height.value,
        length=sld_length.value,
        width=sld_width.value,
        wall=num_wall.value,
    )

    mo.vstack(
        [build["obj"].part, pk.loads(base64.b64decode(build["param"]["code"]))]
    )
    return (build,)


@app.cell
def _():
    return


@app.cell
def _(app, mo):
    # Run the cli application
    if mo.app_meta().mode == "script":
        app()
    return


if __name__ == "__main__":
    app.run()
