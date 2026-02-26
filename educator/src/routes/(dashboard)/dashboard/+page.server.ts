import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	try {
		// Fetch dashboard stats with 30-day period for trends
		const statsResponse = await fetch('http://localhost:8000/api/v1/educator/dashboard/stats/?period=30d');

		// Fetch educator's company-provided courses (server-side)
		let coursesList: any[] = [];
		try {
			const coursesRes = await fetch('http://localhost:8000/api/v1/educator/courses/?page_size=100');
			if (coursesRes.ok) {
				const cbody = await coursesRes.json();
				coursesList = cbody.results || cbody || [];
			}
		} catch (e) {
			console.error('Failed to fetch educator courses:', e);
		}

		if (!statsResponse.ok) {
			if (statsResponse.status === 401) {
				throw redirect(302, '/login/');
			}
			console.error('Failed to fetch dashboard stats:', statsResponse.status);
			return {
				stats: null,
				pipeline: null,
				recentCourses: []
			};
		}

		const data = await statsResponse.json();

		return {
			stats: data.stats,
			pipeline: data.pipeline,
			recentCourses: data.recent_courses || [],
			companyCourses: coursesList,
		};
	} catch (error) {
		if (error instanceof Response && error.status === 302) {
			throw error;
		}
		console.error('Dashboard load error:', error);
		return {
			stats: null,
			pipeline: null,
			recentCourses: [],
			error: 'Failed to load dashboard data'
		};
	}
};
