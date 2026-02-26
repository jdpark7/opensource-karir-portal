from haystack.query import SearchQuerySet
sqs = SearchQuerySet().filter(status="Live").filter(skills__in=['CSS', 'css'])
print(f'Haystack found {len(sqs)} posts')
