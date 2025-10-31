# mocad

[Marimo](https://marimo.io/) for [codecad](https://learn.cadhub.xyz/blog/curated-code-cad/) gives you `mocad`

This is a current experiment of mine to bring codecad into the marimo notebook. Recently marimo has taken off being an alternative to jupyter notebooks. Marimo being reproducable and reactive, I envisaged it's use for codecad. I've already been working with codecad and notebooks via vscodes python execution syntax check out my [CodeCAD repo](https://github.com/andyrobreid/CodeCAD/).
For the CodeCAD end of things I'll be using [build123d](https://github.com/gumyr/build123d) as my preference.

I envisage a use of an [anywidget](https://anywidget.dev/) implementation.

Think of this as a means to have gui's for steps in the design. No need to suppress features like in typical CAD packages. It's like test points on hydraulic circuits to see behaviour at a point. 

# Get Started

To run in notebook edit form and iterate on the design:
    `uv run marimo edit`

To run in script form and get model output: 
    `uv run ./examples/codecad-nb.py --help`


# Roadmap

Currently thinking to:

1. [ ] Three.js anywidget to view objects.
2. [ ] Viewer widget to scale the view according to object loaded.
3. [ ] Take build123d object and pass to widget having it seen. 
4. [ ] Class/Function to wrap around codecad 
  - This would trigger a viewer to be seen for the cell. 
  - When running as a script the wrapper just passes the object as normal to further process.
5. [ ] Selection of geometry elements and providing detail
6. [ ] Selection of geometry elements for identification of how it was produced

## Future
  
With other marimo style widgets the future could entail an interactive gui to provide references for further codecad operations. I'll not bite this off ... yet, too much to chew.

Optimiseation engine to run the geometry build and check for interferance etc on a variable range for design parameters. I've seen this done with solidworks.

- [ ] research what this process is called.

Hybrid with simulations and plots all in the same project/notebook. Nearly like unit tests for designs. This may not live in this repo, maybe a mosim or something.

