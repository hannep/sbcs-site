#!/usr/bin/env python
from sbcswebsite.models import JobPost, db
import sys

job_post_id = raw_input("Enter an id to edit: ")
try:
	edit_id = int(job_post_id)
	job_post = JobPost.query.get(int(edit_id))
except:
	print "Invalid id entered, creating new post"
	job_post = JobPost()

job_post.title = raw_input("Enter a title: ")
print "Enter the contents of the file:"
job_post.content_html = sys.stdin.read()

db.session.add(job_post)
db.session.commit()