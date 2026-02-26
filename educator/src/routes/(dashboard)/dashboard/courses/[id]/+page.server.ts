import type { PageServerLoad } from './$types';
import { redirect, error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, fetch, cookies, url }) => {
    const id = params.id;
    const accessToken = cookies.get('access_token');
    const refreshToken = cookies.get('refresh_token');

    if (!accessToken && !refreshToken) {
        throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
    }

    const apiUrl = `http://localhost:8000/api/v1/educator/courses/${id}/`;
    const res = await fetch(apiUrl);
    if (!res.ok) {
        if (res.status === 401) {
            cookies.delete('access_token', { path: '/' });
            cookies.delete('refresh_token', { path: '/' });
            throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
        }
        if (res.status === 404) throw error(404, 'Course not found');
        throw error(res.status, `Failed to load course: ${res.statusText}`);
    }
    const data = await res.json();
    return { course: data };
};
