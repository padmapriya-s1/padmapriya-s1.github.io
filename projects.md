---
layout: archive
title: "Projects"
permalink: /projects/
author_profile: true
---

{% include base_path %}

{% assign projects = site.projects | sort: "date" | reverse %}

{% for project in projects %}
  {% assign item = project %}
  {% include archive-single.html %}
{% endfor %}
