from django.shortcuts import render, get_object_or_404
from .models import Job, JobCategory


def jobs_list(request):
    """List all jobs"""
    jobs = Job.objects.filter(is_active=True)
    categories = JobCategory.objects.all()
    
    # Filters
    category_slug = request.GET.get('category')
    job_type = request.GET.get('type')
    location = request.GET.get('location')
    
    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    context = {
        'jobs': jobs,
        'categories': categories,
    }
    return render(request, 'jobs/jobs_list.html', context)


def job_detail(request, slug):
    """Job detail page"""
    job = get_object_or_404(Job, slug=slug, is_active=True)
    
    # Increment views
    job.views_count += 1
    job.save(update_fields=['views_count'])
    
    # Related jobs
    related_jobs = Job.objects.filter(
        category=job.category,
        is_active=True
    ).exclude(id=job.id)[:3]
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)
