---
layout: default
img: zork.jpg
img_link: https://en.wikipedia.org/wiki/Zork#/media/
caption: Zork, an early intractive fiction game released in 1977.
title: RL for Language Agents
type: Homework
number: 2
active_tab: homework
release_date: 04-29-2025
due_date: 05-13-2025
materials:
    - 
        name: Text Adventure Game starter code
        url: https://github.com/pearls-lab/intro-deep-rl-course/tree/main/homeworks/hw2
submission_link: https://www.gradescope.com
readings:
    -
      title: Textworld
      authors: Cote et al. 2019
      url: https://github.com/microsoft/TextWorld
---

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

### HW2

HW2 consists of two parts:
- [Part 1: Implementing Q-Learning in TextWorld](https://github.com/pearls-lab/intro-deep-rl-course/blob/main/homeworks/hw2/hw2_part1.ipynb) (50pts)
- [Part 2: Implementing DQN in TextWorld]((https://github.com/pearls-lab/intro-deep-rl-course/blob/main/homeworks/hw2/hw2_part2.ipynb)) (50pts)

Submissions should be done on [Gradescope]({{page.submission_link}}).

## Grading
<div class="alert alert-warning" markdown="1">

</div>

{% if page.readings %} 
## Recommended readings
{% for reading in page.readings %}
* {{ reading.authors }}, <a href="{{ reading.url }}">{{ reading.title }}</a>.  <i>{{ reading.note }}</i>
{% endfor %}
{% endif %}
