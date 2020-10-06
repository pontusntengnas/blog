# coding=utf-8

import os

md_path = '../posts/md'
output_path = '../posts/html'
html_template_path = '../posts/html-template'

post_html_template = """<!DOCTYPE html>
<html>
  <head>
    <title>- {title} {date} | Pontus Tengnäs | Blog -</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" 
      content="I am a full stack software developer based in Gothenburg 
              Sweden and this is my blog where I write about software development and tech">
    <link rel="stylesheet" href="../../style/colors.light.css">
    <link rel="stylesheet" href="../../style/post.style.css">
  </head>
  <body>
    <div class="wrapper">
      <div class="container">
        
        <a href="../../index.html"><h2>- pontusnt blog</h2></a>

        <div class="post-content">
          <h2>{title}</h2>
          <h3>{date}</h3>
          <p>{body}</p>
        </div>

      </div>

      <div class="footer">
        <p>Thanks to <a href="https://cssnano.co/" target="_blank" rel="noreferrer">CSSNANO</a> and <a href="https://github.com/kangax/html-minifier" target="_blank" rel="noreferrer">HTMLMinifier</a> for helping me minifying the CSS and the HTML on this page.</p>
      </div>

    </div>
  </body>
</html>
"""

index_html_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>- Pontus Nilsson Tengnäs | Blog -</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" 
      content="I am a full stack software developer based in Gothenburg 
              Sweden and this is my blog where I write about software development and tech">
    <link rel="stylesheet" href="style/colors.light.css">
    <link rel="stylesheet" href="style/index.style.css">
  </head>
  <body>
    <div class="wrapper">
      <div class="container">
        <picture>
          <source type="image/webp" srcset="images/me.webp">
          <source type="image/jpeg" srcset="images/me.jpg">
          <img src="images/me.jpg" alt="Pontus Nilsson Tengnäs" class="header-picture">
        </picture>

        <h1>Welcome!</h1>

        <p>My name is Pontus Tengnäs and I am a full-stack developer with a primary focus on .NET and web development, based in Gothenburg, Sweden.
          Here I will write about my experiences and insights as I continue walking the never-ending learing-path that is Software Development.</p>

        </br>

        <ul>
          {posts}
        </ul>
      </div>

      <div class="footer">
        <p>Thanks to <a href="https://cssnano.co/" target="_blank" rel="noreferrer">CSSNANO</a> and <a href="https://github.com/kangax/html-minifier" target="_blank" rel="noreferrer">HTMLMinifier</a> for helping me minifying the CSS and the HTML on this page.</p>
      </div>

    </div>
  </body>
</html>"""

def get_file_paths():
  files = []
  for r, _, f in os.walk(md_path):
    for file in f:
        if '.md' in file:
            files.append(os.path.join(r, file))

  return files

def read_file(file):
  blog_post = {'title': '', 'date': '', 'body': ''}
  open_file = open(file, 'r')
  line_count = 0

  file_name = os.path.basename(open_file.name)
  blog_post['date'] = file_name.replace(".md", "")
  
  while True: 
    line = open_file.readline() 
  
    if not line:
      break

    if (line_count == 0):
      blog_post['title'] = line.rstrip('\n')
    if (line_count > 1):
      blog_post['body'] += line.rstrip('\n')

    line_count += 1

  open_file.close()
  return blog_post

def generate_html(blog_post):
  title = blog_post['title']
  date = blog_post['date']
  body = blog_post['body']

  # TODO Handle link
  # TODO Handle image

  return post_html_template.replace('{title}', title).replace('{body}', body).replace('{date}', date)

def format_post_url(blog_post):
  return 'posts/html/{}.html'.format(blog_post['date'].replace('-', ''))

def build_index_link(blog_post):
  return "<li>{} -<a href=\"{}\">{}</a></li>".format(blog_post['date'], format_post_url(blog_post), blog_post['title'])

def write_post_file(blog_post, html):
  post_file = open('{}/{}.html'.format(output_path, blog_post['date'].replace('-', '')), 'w')
  post_file.write(html)
  post_file.close()

def write_index_file(index_html):
  index_file = open('../index.html', 'w')
  index_file.write(index_html)
  index_file.close()

# driver code

files = get_file_paths()

blog_posts = []
blog_posts_html = []
for f in files:
    blog_post = read_file(f)
    blog_posts.append(blog_post)
    h = generate_html(blog_post)
    blog_posts_html.append(h)

post_index = 0
index_links = ''
for p in blog_posts:
  index_links += "{}\n      ".format(build_index_link(p))
  write_post_file(p, blog_posts_html[post_index])
  post_index += 1

index_html = index_html_template.replace("{posts}", index_links.strip())
write_index_file(index_html)