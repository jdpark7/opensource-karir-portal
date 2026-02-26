<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { Button, Card } from '$lib/components/ui';
	import { enhance } from '$app/forms';
	import { invalidate } from '$app/navigation';
	import type { PageData } from './$types';

	export let data: PageData;
	let formResult: any = null;
	let isSubmitting = false;

	// Courses list for the logged-in user's company
	const courses = writable<any[]>([]);
	const loadingCourses = writable(true);
	const coursesError = writable('');

	onMount(async () => {
		loadingCourses.set(true);
		try {
			const res = await fetch('/api/v1/educator/courses/', { credentials: 'include' });
			if (!res.ok) throw new Error(`Failed to load courses (${res.status})`);
			const json = await res.json();
			const list = Array.isArray(json) ? json : json.results || [];
			courses.set(list);
		} catch (e: any) {
			coursesError.set(e?.message || String(e));
		} finally {
			loadingCourses.set(false);
		}
	});

	async function onEnhance() {
		return ({ result, update }: any) => {
			isSubmitting = false;
			update();
			result.formData().then(() => invalidate());
		};
	}
</script>

<svelte:head>
	<title>Courses - InaWorks educator</title>
</svelte:head>

<div class="max-w-3xl mx-auto py-6">
	<!-- Company provided courses -->
	{#if $loadingCourses}
		<div class="mb-4">Loading your company's courses…</div>
	{:else}
		{#if $courses.length > 0}
			<Card padding="md" class="mb-4">
				<h2 class="text-lg font-semibold mb-2">Your Company Courses</h2>
				<ul class="space-y-2">
					{#each $courses as c}
						<li class="flex justify-between items-center">
							<div>
								<div class="font-medium">{c.name}</div>
								<div class="text-sm text-muted">Instructor: {c.instructor}</div>
							</div>
							<div class="flex gap-2">
								<a class="btn" href={`/dashboard/courses/${c.id}`}>View</a>
								<a class="btn btn-primary" href={`/dashboard/courses/${c.id}/edit`}>Edit</a>
							</div>
						</li>
					{/each}
				</ul>
			</Card>
		{:else}
			<div class="mb-4 text-sm text-muted">No courses found for your company.</div>
		{/if}
	{/if}
	<Card padding="md">
		<h1 class="text-2xl font-bold mb-2">Create Course</h1>
		<p class="text-sm text-muted mb-4">Create a new course via API (simple form)</p>

		{#if formResult?.success}
			<div class="bg-success-light border border-success/30 rounded-lg p-3 mb-4">
				<p class="text-success">{formResult.message || 'Created successfully'}</p>
				<p class="text-sm">Course ID: {formResult.courseId}</p>
			</div>
		{/if}

		{#if formResult?.error}
			<div class="bg-error-light border border-error/30 rounded-lg p-3 mb-4">
				<p class="text-error">{formResult.error}</p>
			</div>
		{/if}

		<form method="POST" action="?/create" enctype="multipart/form-data" use:enhance={() => {
			isSubmitting = true;
			return async ({ result, update }: any) => {
				isSubmitting = false;
				const json = await result.json().catch(() => null);
				formResult = json || null;
				update();
			};
		}}>
			<div class="space-y-4">
				<div>
					<label for="name" class="block text-sm font-medium text-muted mb-1">Name</label>
					<input id="name" name="name" required class="w-full px-3 py-2 border rounded" />
				</div>

				<div class="grid grid-cols-2 gap-4">
					<div>
						<label for="slug" class="block text-sm font-medium text-muted mb-1">Slug</label>
						<input id="slug" name="slug" class="w-full px-3 py-2 border rounded" />
					</div>
					<div>
						<label for="instructor" class="block text-sm font-medium text-muted mb-1">Instructor</label>
						<input id="instructor" name="instructor" class="w-full px-3 py-2 border rounded" />
					</div>
				</div>

				<div>
					<label for="provider" class="block text-sm font-medium text-muted mb-1">Provider</label>
					<input id="provider" name="provider" class="w-full px-3 py-2 border rounded" />
				</div>

				<div>
					<label for="url" class="block text-sm font-medium text-muted mb-1">URL</label>
					<input id="url" name="url" class="w-full px-3 py-2 border rounded" />
				</div>

				<div>
					<label for="image" class="block text-sm font-medium text-muted mb-1">Course Image</label>
					<input id="image" name="image" type="file" accept="image/*" class="w-full" />
				</div>

				<div>
					<label for="description" class="block text-sm font-medium text-muted mb-1">Description</label>
					<textarea id="description" name="description" rows="6" class="w-full px-3 py-2 border rounded"></textarea>
				</div>

				<div>
					<label for="keywords" class="block text-sm font-medium text-muted mb-1">Keywords (comma separated)</label>
					<input id="keywords" name="keywords" class="w-full px-3 py-2 border rounded" />
				</div>

				<div>
					<label for="skills" class="block text-sm font-medium text-muted mb-1">Skills (comma separated)</label>
					<textarea id="skills" name="skills" rows="3" class="w-full px-3 py-2 border rounded"></textarea>
				</div>

				<div>
					<label for="status" class="block text-sm font-medium text-muted mb-1">Status</label>
					<select id="status" name="status" class="w-full px-3 py-2 border rounded">
						<option value="Active">Active</option>
						<option value="Inactive">Inactive</option>
					</select>
				</div>

				<div class="flex justify-end gap-2">
					<Button type="submit" disabled={isSubmitting}>Save</Button>
					<Button type="button" variant="secondary" on:click={() => { /* reset form */ (document.querySelector('form') as HTMLFormElement).reset(); }}>Reset</Button>
				</div>
			</div>
		</form>
	</Card>
</div>
