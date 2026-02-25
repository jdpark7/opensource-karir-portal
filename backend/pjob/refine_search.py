from peeldb.models import JobPost, City, Skill, Qualification, Industry, Country
from haystack.query import SQ, SearchQuerySet
from django.db.models import Q


valid_time_formats = ["%Y-%m-%d 00:00:00"]


def refined_search(data):
    searched_skills = searched_locations = searched_industry = searched_edu = (
        Skill.objects.none()
    )
    # Use ORM instead of Haystack to support correct icontains substring matching
    sqs = JobPost.objects.filter(status="Live")
    if "refine_skill" in data and data.getlist("refine_skill"):
        term = data.getlist("refine_skill")
        
        sqs = sqs.filter(
            Q(title__in=term)
            | Q(skills__name__icontains=term[0])
            | Q(description__in=term)
            | Q(job_role__in=term)
            | Q(edu_qualification__name__in=term)
        ).distinct()
        searched_skills = Skill.objects.filter(name__icontains=term[0])

    location = data.getlist("refine_location") if "refine_location" in data else []
    searched_locations = City.objects.filter(name__in=location)
    if "Across India" in location:
        india = Country.objects.filter(name="India")
        sqs = sqs.filter(
            Q(location__state__state__name__in=india.values_list("state__state__name", flat=True))
        ).distinct()
    elif location:
        sqs = sqs.filter(Q(location__name__in=location)).distinct()

    if data.get("job_type"):
        if data["job_type"] == "Fresher":
            sqs = sqs.filter(min_year__lte=0)
        else:
            sqs = sqs.filter(job_type__in=[data["job_type"]])

    if "refine_industry" in data and data.getlist("refine_industry"):
        term = data.getlist("refine_industry")
        sqs = sqs.filter(industry__name__in=term).distinct()
        searched_industry = Industry.objects.filter(name__in=term)

    if "refine_education" in data and data.getlist("refine_education"):
        term = data.getlist("refine_education")
        sqs = sqs.filter(edu_qualification__name__in=term).distinct()
        searched_edu = Qualification.objects.filter(name__in=term)

    if "functional_area" in data and data.getlist("functional_area"):
        term = data.getlist("functional_area")
        sqs = sqs.filter(functional_area__name__in=term).distinct()

    if data.get("refine_experience_min") or data.get("refine_experience_min") == 0:
        sqs = sqs.filter(min_year__lte=int(data["refine_experience_min"]))

    if data.get("refine_experience_max") or data.get("refine_experience_max") == 0:
        sqs = sqs.filter(max_year__lte=int(data["refine_experience_max"]))

    sqs = sqs.select_related("company", "user").prefetch_related("location", "skills", "industry").order_by("-published_on")
    return (
        sqs,
        searched_skills,
        searched_locations,
        searched_industry,
        searched_edu,
    )
