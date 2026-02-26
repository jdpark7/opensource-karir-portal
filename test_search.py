from haystack.query import SearchQuerySet, SQ
from peeldb.models import JobPost

sqs = SearchQuerySet().models(JobPost).filter_and(status="Live")
term = ['CSS']
sqs = sqs.filter_and(
    SQ(title__in=term)
    | SQ(skills__in=term)
    | SQ(description__in=term)
    | SQ(edu_qualification__in=term)
)
print("SQS Count:", sqs.count())
