from datetime import datetime

from praw.models import Submission, Comment as C, MoreComments


class Post:

    def __init__(self, submission: Submission):
        self.id = submission.id
        self.title = submission.title
        self.text = submission.selftext
        self.comments = [Comment(c) for c in submission.comments[:6] if not isinstance(c, MoreComments)]
        self.upvotes = submission.ups
        self.downvotes = submission.downs
        self.is_sticky = submission.stickied
        self.submitted_at = datetime.utcfromtimestamp(submission.created_utc)

    def __eq__(self, other):
        if not isinstance(other, Post):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Comment:

    def __init__(self, comment: C):
        self.id = comment.id
        self.text = comment.body
        self.upvotes = comment.ups
        self.downvotes = comment.downs
        self.submitted_at = datetime.utcfromtimestamp(comment.created_utc)
        self.children = [Comment(r) for r in comment.replies[:3] if not isinstance(r, MoreComments)]


    def __eq__(self, other):
        if not isinstance(other, Comment):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)