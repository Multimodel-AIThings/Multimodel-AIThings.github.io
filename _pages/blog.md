---
layout: default
permalink: /blog/
title: blog
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
    before: 1 # The number of links before the current page
    after: 3 # The number of links after the current page
---

<div class="post">

  <div class="header-bar">
    <h1>{{ page.title }}</h1>
    <h2>Research, Code & Life in our Innovation Lab</h2>
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

  <div class="posts">
    {% assign postlist = page.pagination.enabled and paginator.posts or site.posts %}
    {% for post in postlist %}
    {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
    <div class="post-item">
      <h3 class="post-title">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </h3>
      
      <p class="post-description">{{ post.description }}</p>
      
      <div class="post-meta">
        <span>{{ read_time }} min read</span>
        <span>&bull;</span>
        <span>{{ post.date | date: '%B %d, %Y' }}</span>
        
        {% if post.tags.size > 0 or post.categories.size > 0 %}
          <span>&bull;</span>
          <div class="post-tags">
            {% for tag in post.tags %}
              <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}" class="tag">#{{ tag }}</a>
            {% endfor %}
            {% for category in post.categories %}
              <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}" class="category">{{ category }}</a>
            {% endfor %}
          </div>
        {% endif %}
      </div>
    </div>
    <hr class="post-divider">
    {% endfor %}
  </div>

  {% if page.pagination.enabled %}
    {% include pagination.liquid %}
  {% endif %}

</div>

<footer class="footer">
  <p>© Copyright 2020-2025. AiThings RG AI Innovation Lab. Presented by Jujuj with Studio theme. Hosted by Hotelling Digital Paper. Privacy from Jungleth.</p>
</footer>
