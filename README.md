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

WARNING: I am still in the early days of releasing so it's going to be a few weeks before
this tool is ready to use. I don't recommend wasting your time downloading just yet unless you just want
to play with it and look at the code and documentation. Follow me
on [twitter](https://twitter.com/Leon_Starr) or
[LinkedIn](https://linkedin.com/in/modelint) for updates.

## Shameless plug

In the meantime, if you are curious about the whole MBSE thing that this tool supports, take a look at our [book](https://modelstocode.com).
Also, various resources at the [Model Integration](https://modelint.com/mbse) website.

## Installation

Notes here are for those familiar with python installation procedures.  I will write a more detailed set of procedures
for those who are not in a later release.

Flatland currently uses the multi-platform [cairo graphics library](https://cairographics.org) to do all of the
drawing. Ideally, you should ensure that you have cairo installed before installing Flatland. If you are on Mac OS X,
you can use homebrew to install it easily. (It worked fine for me, anyway)

You should also ensure that you have Python 3.9+ installed. A virtual environment is highly recommended.

You can install the Flatland Model Diagram Editor from [PyPI](https://pypi.org/project/flatland-model-diagram-editor/):

    $ pip install flatland-model-diagram-editor

Flatland is supported on Python 3.9 and above

## How to use

Assuming you have two files, my_model.xmm (xmm = Executable Model Markdown) and my_layout.xss (xss = Executable model Style Sheet),

    $ flatland -m my_model.xmm -l my_layout.xss -d my_beautiful_diagram.pdf

The use of standard input / output is not yet supported so all files must be supplied as parameters.
If no files are specified, the following default names will be assumed 'model.xmm', 'layout.xss' and
'diagram.pdf'.

## Model and layout files

Initially I will be supplying a grammar/parser for specifying model layouts. It knows all about nodes, connectors
of various types and uses a system for placement of nodes and connector anchors that doesn't require you to know
anything about pixels or points. We use an agile system of relative placement that is extremely awesome!

The grammar is a PEG grammar defined using the arpeggio python package.

The model grammar/parser, also provided, is specifically for xUML model semantics. If you have some other modeling
language that you want to draw, no worries. You can use the template to create your own grammar. You will need
to get comfortable with arpeggio and PEG grammars, but you're a smart engineer and I know you can do it!

## Schedule

I am in the process of upgrading the test framework, usage documentation and support for more diagram types.
A version you can actually use to do something useful probably won't be available until early February 2021.

Expect this to be in serious beta by late spring 2021. I would like it to be sooner, but I
have [a day job](https://www.tri.global/).
