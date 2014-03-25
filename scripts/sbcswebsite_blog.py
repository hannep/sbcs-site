#!/usr/bin/env python
from sbcswebsite.models import BlogPost, db
import sys

blog_post_id = raw_input("Enter an id to edit: ")
try:
	edit_id = int(blog_post_id)
	blog_post = BlogPost.query.get(int(edit_id))
except:
	print "Invalid id entered, creating new post"
	blog_post = BlogPost()

blog_post.title = raw_input("Enter a title: ")
print "Enter the contents of the file:"
blog_post.content_html = sys.stdin.read()

db.session.add(blog_post)
db.session.commit()