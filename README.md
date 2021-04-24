# Flatland Model Diagram (non) Editor

Ah yes, yet another tool for generating diagrams from text. But this one is different (otherwise I wouldn't have wasted all this time building it!)

I built Flatland because the following benefits are critical for productive model development:

1. Complete separation of the model semantics from the diagram layout
2. Complete separation of model semantics from model notation
3. Consistent layout of model diagrams without forcing the user to accept or hack awkard, non-sensical placements of nodes and connectors (yeah, I'm lookin at YOU PlantUML)
4. Maximum layout power with minimal specification:  No more carpal tunnel pixel pushing!
5. Beautiful, readable diagram output in many output formats (pdf, svg, etc)
6. Support for industrial strength modeling (many hundreds and thousands of model elements
7. Use your favorite text editor and all the advanced facilities of it and whatever IDE you like without having to learn yet another draw tool that makes you and your team's life difficult.
8. And since we're here on GitHub, wouldn't it be nice if all of your models were under proper configuration management where you and your team can diff and merge to your heart's content? Wouldn't it be nice to update a diagram layout without touching the underlying model (and vice versa)?

Basically, I have wasted way too many hours of my career pushing pixels around and I just couldn't take it anymore!

Flatland is a model diagram non-editor written by me [Leon Starr](mailto:leon_starr@modelint.com) that generates
beautiful PDFs (and other output formats) based on two very
human-readable input text files. The model file specifies model semantics
(state transitions, generalizations, classes etc)
while the layout file specifies (node placement and alignment, connector anchors) and lightly refers to some elements
in the model file. You can think of the layout file as a "style sheet" for your models.
Some benefits:

WARNING: I am still in the early days of releasing to the greater public so it's going to be a few weeks/months before
this tool is ready for the outside world. We are currently using it at the Toyota Research Institute for our work modeling the driving environment for autonomous vehicles. So this tool is in production and improving daily. Nonetheless, I don't recommend wasting your time downloading just yet unless you just want
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

Assuming you have two files, my_model.xmm (xmm = Executable Model Markdown) and my_layout.mss (mss = Model Style Sheet),
and you would like a generated pdf diagram named 'my_beautiful_diagram.pdf', type this:

    $ flatland -m my_model.xmm -l my_layout.mss -d my_beautiful_diagram.pdf

The use of standard input / output is not yet supported so all files must be supplied as parameters.
All arguments are optional. If no files are specified, the following default names will be assumed 'model.xmm',
'layout.xss' and 'diagram.pdf'. The command will fail, however, if the first two files are not found in the current
directory.

To get a local copy of the example model and layout file directory, use the -E option. The -D option gets you a local
copy of the documentation direcotry including the models used to design flatland itself. Type the following to get
both directories:

    $ flatland -E -D

Inside the examples directory you will find a copy of the test script used to test all of the examples. It won't run
locally, but you can look inside this file to see which model and layout files pair together. For example, you
can see that test `t001` pairs the `aircraft2.xmm` model with the `t001_straight_binary_horiz.mss` layout. At this
point there is no documentation available on the xmm scripting language or the mss layout language, but you should
be able to figure them out by scanning the examples and comparing with generated pdf output. Have fun with that.

Don't worry, more documentation is coming soon.

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
