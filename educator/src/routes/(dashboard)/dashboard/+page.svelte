<script lang="ts">
	import { Briefcase, FileText, TrendingUp, Clock } from '@lucide/svelte';
	import { Button, Card, Badge } from '$lib/components/ui';
	import type { PageData } from './$types';

	export let data: PageData;

	// Top courses (will load educator's company-provided online courses)
	// Use server-provided courses list (companyCourses) to avoid client-side proxy issues
	// raw list from server mapped into the shape we use
	$: topCourses = (data.companyCourses || []).filter((c: any) => c.url).map((c: any) => ({
		id: c.id,
		title: c.name,
		instructor: c.instructor,
		provider: (c.provider_name || (c.provider && c.provider.name) || c.provider),
		status: c.status,
		created_at: c.created_at
	}));

	// Client-side controls
	let searchTerm = '';
	let statusFilter = 'All';
	let ordering = '-created_at';

	// Filtered and ordered list derived from topCourses
	$: filteredCourses = topCourses
		.filter((c: any) => {
			const q = searchTerm.trim().toLowerCase();
			if (!q) return true;
			return (
				(c.title || '').toLowerCase().includes(q) ||
				(c.instructor || '').toLowerCase().includes(q) ||
				(String(c.provider || '') || '').toLowerCase().includes(q)
			);
		})
		.filter((c: any) => (statusFilter === 'All' ? true : c.status === statusFilter))
		.slice()
		.sort((a: any, b: any) => {
			if (ordering === 'title') return a.title.localeCompare(b.title);
			if (ordering === '-title') return b.title.localeCompare(a.title);
			if (ordering === 'created_at') return ('' + a.created_at).localeCompare(b.created_at);
			// default '-created_at'
			return ('' + b.created_at).localeCompare(a.created_at);
		});

	function getJobStatusVariant(status: string): 'success' | 'warning' | 'error' | 'neutral' {
		const variants: Record<string, 'success' | 'warning' | 'error' | 'neutral'> = {
			Live: 'success',
			Draft: 'neutral',
			Disabled: 'error',
			Expired: 'warning'
		};
		return variants[status] || 'neutral';
	}
</script>

<svelte:head>
	<title>Dashboard - InaWorks educator</title>
</svelte:head>

<div class="space-y-6">
	<!-- Recent Courses Only -->
	<Card padding="none">
		<div class="p-6 border-b border-border">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-semibold text-black">Courses</h2>
				<div class="flex items-center gap-4">
					<a href="/dashboard/courses/" class="text-sm text-primary hover:text-primary-hover font-medium transition-colors">
						View all courses
					</a>
					<div class="flex items-center gap-2">
						<input
							type="search"
							placeholder="Search courses, instructor, provider"
							bind:value={searchTerm}
							class="px-3 py-1 border rounded-md text-sm"
						/>
						<select bind:value={statusFilter} class="px-2 py-1 border rounded-md text-sm">
							<option value="All">All</option>
							<option value="Active">Active</option>
							<option value="Inactive">Inactive</option>
						</select>
						<select bind:value={ordering} class="px-2 py-1 border rounded-md text-sm">
							<option value="-created_at">Newest</option>
							<option value="created_at">Oldest</option>
							<option value="title">Title A→Z</option>
							<option value="-title">Title Z→A</option>
						</select>
					</div>
				</div>
			</div>
		</div>
		{#if filteredCourses.length > 0}
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-surface border-b border-border">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Course Title</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Instructor</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Provider</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Status</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-border">
						{#each filteredCourses as course}
							<tr class="hover:bg-surface transition-colors">
								<td class="px-6 py-4">
									<a href="/dashboard/courses/{course.id}/" class="text-sm font-medium text-primary hover:text-primary-hover transition-colors">{course.title}</a>
								</td>
								<td class="px-6 py-4 text-sm text-muted">{course.instructor}</td>
								<td class="px-6 py-4 text-sm text-muted">{course.provider}</td>
								<td class="px-6 py-4 text-sm">
									<Badge variant={getJobStatusVariant(course.status)}>{course.status}</Badge>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="p-12 text-center">
				<Briefcase class="w-12 h-12 text-muted mx-auto mb-3" />
				{#if searchTerm || statusFilter !== 'All'}
					<p class="text-muted mb-4">No courses match your filters.</p>
				{:else}
					<p class="text-muted mb-4">No online courses provided by your organization yet.</p>
				{/if}
			</div>
		{/if}
	</Card>
</div>
