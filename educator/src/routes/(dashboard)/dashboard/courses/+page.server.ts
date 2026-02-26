import type { PageServerLoad } from './$types';
import { redirect, error } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/config/env';

import type { Actions } from './$types';

export const load: PageServerLoad = async ({ fetch, url, cookies }) => {
    const accessToken = cookies.get('access_token');
    const refreshToken = cookies.get('refresh_token');

    if (!accessToken && !refreshToken) {
        throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
    }

    const page = url.searchParams.get('page') || '1';
    const page_size = url.searchParams.get('page_size') || '20';
    const search = url.searchParams.get('search') || '';

    try {
        const params = new URLSearchParams({ page, page_size });
        if (search) params.append('search', search);

        // Allow fetching to use the correct base URL whether local or remote
        const apiUrl = `${API_BASE_URL}/educator/courses/?${params.toString()}`;

        // Pass the auth token in headers since this request goes to another domain/proxy potentially
        const res = await fetch(apiUrl, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!res.ok) {
            // Error handling needs to actually throw the error, not just define it
            if (res.status === 401) {
                // Delete cookies without extra options since we are using fetch
                cookies.delete('access_token', { path: '/' });
                cookies.delete('refresh_token', { path: '/' });
                throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
            }
            throw error(res.status, `Failed to load courses: ${res.statusText}`);
        }

        const data = await res.json();


        return {
            courses: data.results || data || [],
            count: data.count || (data.results && data.results.length) || 0,
            next: data.next || null,
            previous: data.previous || null,
            currentPage: parseInt(page),
            filters: { search }
        };
    } catch (err: any) {
        console.error('Error loading courses:', err);
        if (err.status === 302) throw err;
        throw error(500, err.message || 'Failed to load courses');
    }
};

// Action to create a new course via backend API
export const actions: Actions = {
    create: async ({ request, fetch, cookies, url }) => {
        const accessToken = cookies.get('access_token');
        const refreshToken = cookies.get('refresh_token');

        if (!accessToken && !refreshToken) {
            throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
        }

        const incoming = await request.formData();

        // Build FormData to forward to backend (multipart/form-data)
        const fd = new FormData();

        // Map expected fields from the admin screenshot
        const mapping = [
            'name',
            'slug',
            'instructor',
            'provider',
            'url',
            'description',
            'keywords',
            'skills',
            'status'
        ];

        for (const key of mapping) {
            const v = incoming.get(key);
            if (v !== null) fd.append(key, String(v));
        }

        // Handle image/file upload (field name: image or course_img)
        const img = incoming.get('image') || incoming.get('course_img');
        if (img && typeof img !== 'string') {
            // append Blob/File directly
            fd.append('image', img as Blob);
        }

        try {
            const apiUrl = `${API_BASE_URL}/educator/courses/`;
            const res = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                },
                body: fd
            });

            if (!res.ok) {
                if (res.status === 401) {
                    cookies.delete('access_token', { path: '/' });
                    cookies.delete('refresh_token', { path: '/' });
                    throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
                }
                const text = await res.text();
                return new Response(JSON.stringify({ success: false, error: `API error ${res.status}: ${text}` }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            }

            const data = await res.json();
            return new Response(JSON.stringify({ success: true, courseId: data.id, message: 'Course created' }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        } catch (err: any) {
            console.error('Error creating course:', err);
            return new Response(JSON.stringify({ success: false, error: err.message || 'Failed to create course' }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }
    }
};
