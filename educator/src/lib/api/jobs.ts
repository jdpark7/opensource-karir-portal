/**
 * Job Management API Client
 */
import { apiClient } from './client';
import type {
	CoursesListResponse,
	JobDetail,
	JobCreateData,
	JobUpdateData,
	JobApplicantsResponse,
	DashboardStatsResponse,
	JobFilters,
} from '$lib/types';

/**
 * Get dashboard statistics
 */
export async function getDashboardStats(): Promise<DashboardStatsResponse> {
	return apiClient.get('/educator/dashboard/stats/');
}

/**
 * List all courses posted by the educator
 */
export async function listCourses(filters?: JobFilters): Promise<CoursesListResponse> {
	const params = new URLSearchParams();

	if (filters) {
		if (filters.status) params.append('status', filters.status);
		if (filters.search) params.append('search', filters.search);
		if (filters.ordering) params.append('ordering', filters.ordering);
		if (filters.page) params.append('page', filters.page.toString());
		if (filters.page_size) params.append('page_size', filters.page_size.toString());
	}

	const queryString = params.toString();
	const url = `/educator/courses/${queryString ? `?${queryString}` : ''}`;

	return apiClient.get(url);
}

/**
 * Get job details
 */
export async function getJob(jobId: number): Promise<JobDetail> {
	return apiClient.get(`/educator/courses/${jobId}/`);
}

/**
 * Create a new job
 */
export async function createJob(data: JobCreateData): Promise<{ success: boolean; job: JobDetail; message: string }> {
	return apiClient.post('/educator/courses/create/', data);
}

/**
 * Update an existing job
 */
export async function updateJob(
	jobId: number,
	data: JobUpdateData
): Promise<{ success: boolean; job: JobDetail; message: string }> {
	return apiClient.patch(`/educator/courses/${jobId}/update/`, data);
}

/**
 * Delete a job
 */
export async function deleteJob(jobId: number, force = false): Promise<{ success: boolean; message: string }> {
	const url = `/educator/courses/${jobId}/delete/${force ? '?force=true' : ''}`;
	return apiClient.delete(url);
}

/**
 * Publish a draft job
 */
export async function publishJob(jobId: number): Promise<{ success: boolean; job: JobDetail; message: string }> {
	return apiClient.post(`/educator/courses/${jobId}/publish/`, {});
}

/**
 * Close an active job
 */
export async function closeJob(jobId: number): Promise<{ success: boolean; job: JobDetail; message: string }> {
	return apiClient.post(`/educator/courses/${jobId}/close/`, {});
}

/**
 * Get job applicants
 */
export async function getJobApplicants(
	jobId: number,
	filters?: { status?: string; ordering?: string }
): Promise<JobApplicantsResponse> {
	const params = new URLSearchParams();

	if (filters) {
		if (filters.status) params.append('status', filters.status);
		if (filters.ordering) params.append('ordering', filters.ordering);
	}

	const queryString = params.toString();
	const url = `/educator/courses/${jobId}/applicants/${queryString ? `?${queryString}` : ''}`;

	return apiClient.get(url);
}

/**
 * Get job form metadata (countries, states, cities, skills, industries, qualifications, functional areas)
 */
export async function getJobFormMetadata(filters?: {
	country_id?: number;
	state_id?: number;
	search?: string;
}): Promise<import('$lib/types').JobFormMetadata> {
	const params = new URLSearchParams();

	if (filters) {
		if (filters.country_id) params.append('country_id', filters.country_id.toString());
		if (filters.state_id) params.append('state_id', filters.state_id.toString());
		if (filters.search) params.append('search', filters.search);
	}

	const queryString = params.toString();
	const url = `/educator/courses/metadata/${queryString ? `?${queryString}` : ''}`;

	return apiClient.get(url);
}
