<script lang="ts">
  export let data: any;
  let formResult: any = null;
  let isSubmitting = false;
</script>

<svelte:head>
  <title>Edit Course — {data.course.name}</title>
</svelte:head>

<div class="max-w-3xl mx-auto py-6">
  <h1 class="text-2xl font-bold mb-4">Edit: {data.course.name}</h1>

  {#if formResult?.error}
    <div class="text-red-600 mb-4">{formResult.error}</div>
  {/if}

  <form method="POST" enctype="multipart/form-data">
    <div class="space-y-3">
      <div>
        <label class="block text-sm">Name</label>
        <input name="name" value={data.course.name} class="w-full px-3 py-2 border rounded" />
      </div>
      <div>
        <label class="block text-sm">Instructor</label>
        <input name="instructor" value={data.course.instructor} class="w-full px-3 py-2 border rounded" />
      </div>
      <div>
        <label class="block text-sm">Provider</label>
        <input name="provider" value={data.course.provider} class="w-full px-3 py-2 border rounded" />
      </div>
      <div>
        <label class="block text-sm">URL</label>
        <input name="url" value={data.course.url} class="w-full px-3 py-2 border rounded" />
      </div>
      <div>
        <label class="block text-sm">Description</label>
        <textarea name="description" rows={6} class="w-full px-3 py-2 border rounded">{data.course.description}</textarea>
      </div>
      <div>
        <label class="block text-sm">Image</label>
        <input name="image" type="file" accept="image/*" />
      </div>

      <div class="flex gap-2">
        <button class="btn btn-primary" type="submit">Save</button>
        <a class="btn" href="/dashboard/courses/{data.course.id}">Cancel</a>
      </div>
    </div>
  </form>
</div>
