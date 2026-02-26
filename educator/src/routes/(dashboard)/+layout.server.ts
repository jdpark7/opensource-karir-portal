/**
 * Dashboard Layout Server Load
 * Fetches user data on every page load (including reloads)
 * Uses JWT from HttpOnly cookies to authenticate with Django API
 */

import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { getApiBaseUrl } from '$lib/config/env';

export const load: LayoutServerLoad = async ({ cookies, fetch }) => {
	// Check if user has auth cookies
	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');

	// If no tokens, redirect to login (should be caught by hooks, but double-check)
	if (!accessToken && !refreshToken) {
		throw redirect(302, '/login/');
	}

	try {
		// Validate API base URL
		const baseUrl = getApiBaseUrl();
		if (!baseUrl || typeof baseUrl !== 'string') {
			console.error('Invalid API base URL:', baseUrl);
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			throw redirect(302, '/login/');
		}

		// Normalize URL (avoid double slashes)
		const apiUrl = `${baseUrl.replace(/\/+$|\s+/g, '')}/educator/auth/me/`;

		// Fetch current user from Django API
		// The apiHandler in hooks.server.ts will automatically add the Authorization header
		const response = await fetch(apiUrl);

		if (!response.ok) {
			console.error('API responded with error:', response.status, await safeText(response));
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			throw redirect(302, '/login/');
		}

		// Ensure response is JSON before parsing (protect against HTML error pages)
		const contentType = response.headers.get('content-type') || '';
		if (!contentType.includes('application/json')) {
			console.error('Unexpected response content-type, expected JSON but got:', contentType, await safeText(response));
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			throw redirect(302, '/login/');
		}

		let user;
		try {
			user = await response.json();
		} catch (err) {
			console.error('Failed to parse JSON response:', err, await safeText(response));
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			throw redirect(302, '/login/');
		}

		return { user };
	} catch (error) {
		console.error('Failed to load user:', error);
		cookies.delete('access_token', { path: '/' });
		cookies.delete('refresh_token', { path: '/' });
		throw redirect(302, '/login/');
	}
};

// Helper to safely read response text without throwing on binary responses
async function safeText(res: Response): Promise<string | null> {
    try {
        return await res.clone().text();
    } catch {
        return null;
    }
}
