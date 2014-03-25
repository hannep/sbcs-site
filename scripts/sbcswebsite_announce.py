#!/usr/bin/env python
from sbcswebsite.models import Announcement, db
import sys

announce_id = raw_input("Enter an id to edit: ")
try:
	edit_id = int(announce_id)
	announcement = Announcement.query.get(int(edit_id))
except:
	announce_id = 0
	print "Invalid id entered, creating new post"
	announcement = Announcement()

announcement.title = raw_input("Enter a title: ")
print "Enter the contents of the file:"
announcement.content_html = sys.stdin.read()

db.session.add(announcement)
db.session.commit()