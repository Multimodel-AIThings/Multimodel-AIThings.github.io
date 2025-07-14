---
layout: default
permalink: /blog/
title: Blog – Research, Code & Life @ AiThings
nav: true
nav_order: 1
pagination:
  enabled: true
  collection: posts
  permalink: /page/:num/
  per_page: 5
  sort_field: date
  sort_reverse: true
  trail:
    before: 1
    after: 3
---

<div class="post">

<div class="header-bar">
  <h1>Blog @ AiThings RG</h1>
  <h2>Sharing our research, code, experiments, and life in the lab</h2>
</div>

{% if site.display_tags or site.display_categories %}
  <div class="tag-category-list">
    <ul class="p-0 m-0">
      {% for tag in site.display_tags %}
        <li><i class="fa-solid fa-hashtag fa-sm"></i> 
          <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}">{{ tag }}</a>
        </li>
        {% unless forloop.last %}<p>&bull;</p>{% endunless %}
      {% endfor %}
      {% if site.display_categories and site.display_categories.size > 0 %}
        <p>&bull;</p>
      {% endif %}
      {% for category in site.display_categories %}
        <li><i class="fa-solid fa-tag fa-sm"></i> 
          <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}">{{ category }}</a>
        </li>
        {% unless forloop.last %}<p>&bull;</p>{% endunless %}
      {% endfor %}
    </ul>
  </div>
{% endif %}

{% assign featured_posts = site.posts | where: "featured", "true" %}
{% if featured_posts.size > 0 %}
<br>
<div class="container featured-posts">
  {% assign is_even = featured_posts.size | modulo: 2 %}
  <div class="row row-cols-{% if featured_posts.size <= 2 or is_even == 0 %}2{% else %}3{% endif %}">
    {% for post in featured_posts %}
    <div class="col mb-4">
      <a href="{{ post.url | relative_url }}">
        <div class="card hoverable">
          <div class="row g-0">
            <div class="col-md-12">
              <div class="card-body">
                <div class="float-right"><i class="fa-solid fa-thumbtack fa-xs"></i></div>
                <h3 class="card-title">{{ post.title }}</h3>
                <p class="card-text">{{ post.description }}</p>
                {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
                <p class="post-meta">{{ read_time }} min read · <i class="fa-solid fa-calendar fa-sm"></i> {{ post.date | date: "%Y" }}</p>
              </div>
            </div>
          </div>
        </div>
      </a>
    </div>
    {% endfor %}
  </div>
</div>
<hr>
{% endif %}

<ul class="post-list">
  {% assign postlist = page.pagination.enabled and paginator.posts or site.posts %}
  {% for post in postlist %}
  {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
  <li>
    <h3>
      <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <p>{{ post.description }}</p>
    <p class="post-meta">
      {{ read_time }} min read · {{ post.date | date: '%B %d, %Y' }}
    </p>
    <p class="post-tags">
      {% assign year = post.date | date: "%Y" %}
      <a href="{{ year | prepend: '/blog/' | relative_url }}"><i class="fa-solid fa-calendar fa-sm"></i> {{ year }}</a>
      {% if post.tags.size > 0 %}
        ·
        {% for tag in post.tags %}
          <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}"><i class="fa-solid fa-hashtag fa-sm"></i> {{ tag }}</a>
        {% unless forloop.last %}&nbsp;{% endunless %}
        {% endfor %}
      {% endif %}
      {% if post.categories.size > 0 %}
        ·
        {% for category in post.categories %}
          <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}"><i class="fa-solid fa-tag fa-sm"></i> {{ category }}</a>
        {% unless forloop.last %}&nbsp;{% endunless %}
        {% endfor %}
      {% endif %}
    </p>
  </li>
  {% endfor %}
</ul>

{% if page.pagination.enabled %}
  {% include pagination.liquid %}
{% endif %}

</div>
