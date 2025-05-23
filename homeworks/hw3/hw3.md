---
layout: default
caption: Let's build our own AI Dungeon!
title: Building an AI Game Master
type: Homework
img: mouse_character_image_small.png
caption: Mausritter character portrait
number: 3
active_tab: homework
release_date: 2025-05-16
due_date: 2025-05-30 23:59:00
materials:
   -
      name: hw3-aidm.ipynb
      url: https://github.com/pearls-lab/intro-deep-rl-course/tree/main/homeworks/hw3/hw3-aidm.ipynb
submission_link: https://www.gradescope.com
readings:
  - title: Kani&colon; A Lightweight and Highly Hackable Framework for Building Language Model Applications
    authors: Andrew Zhu, Liam Dugan, Alyssa Hwang, Chris Callison-Burch
    venue: NLP-OSS @ EMNLP
    year: 2024
    type: paper
    url: https://aclanthology.org/2023.nlposs-1.8/
---

<div class="alert alert-info">
This assignment is due on {{ page.due_date | date: "%A, %B %-d, %Y" }} before {{ page.due_date | date: "%I:%M%p" }}. 
</div>

{% if page.materials %}
<div class="alert alert-info">
You can download the materials for this assignment here:
<ul>
{% for item in page.materials %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}


{{page.type}} {{page.number}}: {{page.title}}
=============================================================

*Credits to Original Author: Andrew Zhu (andrz@seas.upenn.edu)*

In this homework, we'll use Kani to build a simple Game Master (GM) for
the [Mausritter TTRPG](https://losing-games.itch.io/mausritter). Your GM will help walk you through creating a mouse and
rolling dice to overcome challenges in the game. Along the way, you'll learn the basics of
the [Kani library](https://kani.readthedocs.io/en/latest/), function calling with LLMs, and how a LLM can use structured
information to act as a game state manager.

We won't implement more complex systems like combat or spellcasting in this homework, but extending this system to make
a more comprehensive GM (e.g. adding inventory tracking, combat, spellcasting, structured tracking of NPCs, ...) would
make for a great class final project.

This assignment will have 3 main parts:

1. **Gain familiarity with Kani and function calling** - You will learn how Kani can be used to expose external APIs to
   LLMs by connecting GPT-4 with a dice rolling library.
2. **Use function calling to build a character creator agent** - We'll show how LLMs can be used to generate structured
   data by creating an agent to walk a new player through the Mausritter character creation process. Your agent will be
   able to roll dice for the player, help translate natural language to game mechanics, and save their character sheet
   once it's created.
3. **Put everything together in an AI GM** - We'll use function calling and the structured character created by
   your agent to create a grounded AI GM. It will have the ability to reference your character sheet and roll saves
   based on your mouse's stats. Finally, we'll see how a grounded AI GM compares to a prompting-only approach. 

## What You'll Need

- A copy of the [Mausritter rules](https://losing-games.itch.io/mausritter) (available for free on itch.io)
- Your [Open AI API key](https://platform.openai.com/api-keys)
- The [Kani documentation](https://kani.readthedocs.io/en/latest/)
- The [d20 documentation](https://d20.readthedocs.io/en/latest/start.html)

### Using our Starter code

We have provided [a Python Notebook for HW3]({{page.materials[0].url}}). I recommend using Visual Studio Code
for this homework. You'll be making changes to the `hw3-aidm.ipynb` file. You should read through the whole Python Notebook
carefully, and add your code to all places marked TODO.

#### Environment Setup

To run this code in your Python IDE, you'll need to install a couple python packages via `pip`, and you'll need to set
the `OPENAI_API_KEY` environment variable to your OpenAI API key.

First [download the notebook]({{page.materials[0].url}}), then create a virtual environment and install
the dependencies. Here's how I recommend that you set up your environment:

```shell
$ mkdir hw3
$ cd hw3
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ pip install jupyter 'kani[openai]' d20
```

If you're using VS code then you can send your OPENAI_API_KEY to it when you launch it from
the command line:

```
$ cd path/to/hw3
$ source venv/bin/activate
(venv) $ OPENAI_API_KEY=sk-helicone-XXXXXXX-XXXXXX code .
```

You should replace `sk-helicone-XXXXXXX-XXXXXX` with your OpenAI API key which you can
find [here](https://platform.openai.com/api-keys).

## What to submit

Please submit the following:

- the notebook `hw3-aidm.ipynb` with all TODOs and free-response sections completed
- the latest saved transcripts of your character creator agent and play (with a structured and unstructured AI GM)
- the image(s) you generated of your character


# Recommended readings

<table>
   {% for publication in page.readings %}
    <tr>
      <td>
	{% if publication.url %}
		<a href="{{ publication.url }}">{{ publication.title }}</a>
        {% else %}
		{{ publication.title }}
	{% endif %}
	{% if publication.authors %}	      
		- {{ publication.authors }}.
	{% endif %}
	{% if publication.year %}	
		{{ publication.venue }}  {{ publication.year }}.
	{% endif %}

	{% if publication.abstract %}
	<!-- abstract button -->
	<a data-toggle="modal" href="#{{publication.id}}-abstract" class="label label-success">Abstract</a>
	<!-- /.abstract button -->
	<!-- abstract content -->
	<div id="{{publication.id}}-abstract" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="{{publication.id}}">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="{{publication.id}}">{{publication.title}}</h4>
        </div><!-- /.modal-header -->
        <div class="modal-body">
        {{publication.abstract}}
        </div><!-- /.modal-body -->
	</div><!-- /.modal-content -->
	</div><!-- /.modal-dialog -->
	</div><!-- /.abstract-content -->
	{% endif %}
	{% if publication.bibtex %}
	<!-- bibtex button -->
	<a data-toggle="modal" href="#{{publication.id}}-bibtex" class="label label-default">BibTex</a>
	<!-- /.bibtex button -->
	<!-- bibtex content -->
	<div id="{{publication.id}}-bibtex" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="{{publication.id}}">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="{{publication.id}}">{{publication.title}}</h4>
        </div><!-- /.modal-header -->
        <div class="modal-body">
 	   <pre>{{publication.bibtex}}
           </pre>
        </div><!-- /.modal-body -->
	</div><!-- /.modal-content -->
	</div><!-- /.modal-dialog -->
	</div><!-- /.bibtex-content -->
	{% endif %}

</td></tr>
  {% endfor %}
</table>
