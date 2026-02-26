<script lang="ts">
  export let data: any;
</script>

<svelte:head>
  <title>Course — {data.course.name}</title>
</svelte:head>

<div class="max-w-3xl mx-auto py-6">
  <div class="mb-4">
    <h1 class="text-2xl font-bold">{data.course.name}</h1>
    <div class="text-sm text-muted">Instructor: {data.course.instructor}</div>
    <div class="text-sm text-muted">Provider: {data.course.provider}</div>
  </div>

  <div class="prose">
    {@html data.course.description || ''}
  </div>

  <div class="mt-4 flex gap-2">
    <a class="btn" href="/dashboard/courses/{data.course.id}">Refresh</a>
    <a class="btn btn-primary" href="/dashboard/courses/{data.course.id}/edit">Edit</a>
  </div>
</div>
