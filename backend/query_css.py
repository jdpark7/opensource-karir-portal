from pjob.models import Skill
print(list(Skill.objects.filter(slug__iexact='css').values('id', 'name', 'slug', 'status')))
