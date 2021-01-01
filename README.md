# Flatland Model Diagram (non) Editor

I built this tool because I want beautiful, human readable model diagram layouts. PlantUML (and its ilk), especially for large,
detailed non-hierarchical diagrams do not deliver. Also, I have wasted way too many hours of my career pushing
pixels around in both proprietary and open source diagram editors and I am sick of it!  No mas!!!
I need to be able to quickly edit and change complex model diagrams, keep them under configuration management,
and integrate them into our open source code/documentation generation pipeline.

Flatland is a model diagram non-editor written by myself [Leon Starr](mailto:leon_starr@modelint.com) that generates
beautiful PDFs (and other output formats) based on two very
human-readable input text files. The model file specifies model semantics
(state transitions, generalizations, classes etc)
while the layout file specifies (node placement and alignment, connector anchors) and lightly refers to some elements
in the model file. You can think of the layout file as a "style sheet" for your models.
Some benefits:

* You can now put your models under configuration management since the source is all text.
* Complex model layouts are easily edited without the need for tedious pixel pushing in a graphical editor
* Executable UML (xUML) in particular is supported, but any similar kind of model diagrams can be supported with
minor extensions
  
In fact, you edit the models and layout in your favorite text editor and then a diagram is generated. So,
technically, this is not an editor at all, but a diagram generator. That said, the generator and associated
model and layout grammar/parsers effectively set you up with a powerful open source model editor.

WARNING: I am in the process of figuring out PyPI for the first time, so it's going to be a few weeks before
this tool is ready to use. I don't recommend wasting your time downloading just yet. Follow me
on [twitter](https://twitter.com/Leon_Starr) or
[LinkedIn](https://linkedin.com/in/modelint) for updates. I do have a nice alpha version working that makes awesome class diagrams in my cozy PyCharm
environment, but it turns out that multi-platform deployment is a pain in the ass. Who knew? ;)

## Shameless plug

In the meantime, if you are curious about the whole MBSE thing that this tool supports, take a look at our [book](https://modelstocode.com).
Also, various resources at the [Model Integration](https://modelint.com/mbse) website.

## Installation

You can install the Flatland Model Diagram Editor from [PyPI](https://pypi.org/project/flatland-model-diagram-editor/):

    pip install flatland-model-diagram-editor

Flatland is supported on Python 3.7 and above

## How to use

Assuming you have two files, my_model.xmm (xmm = Executable Model Markdown) and my_layout.xss (xss = Executable model Style Sheet),

    $ flatland -m my_model.xmm -l my_layout.xss -d my_beautiful_diagram.pdf

Or the model can be standard input and the diagram can go to standard output:

    $ my_model.xmm > flatland -l my_layout.xss > my_beautiful_diagram.pdf

## Model and layout files

Initially I will be supplying a grammar/parser for specifying model layouts. It knows all about nodes, connectors
of various types and uses a system for placement of nodes and connector anchors that doesn't require you to know
anything about pixels or points. We use an agile system of relative placement that is extremely awesome!

The grammar is a PEG grammar defined using the arpeggio python package.

The model grammar/parser, also provided, is specifically for xUML model semantics. If you have some other modeling
language that you want to draw, no worries. You can use the template to create your own grammar. You will need
to get comfortable with arpeggio and PEG grammars, but you're a smart engineer and I know you can do it!

## Schedule

I will be futzing around with PyPI, manifests, documentation, relative imports and so forth into early February 2021,
so a version you can actually use to do something useful probably won't be available until then.

Expect this to be in serious beta by late spring 2021. I would like it to be sooner, but I
have [a day job](https://www.tri.global/).
