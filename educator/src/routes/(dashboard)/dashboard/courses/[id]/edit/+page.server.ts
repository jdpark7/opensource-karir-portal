import type { PageServerLoad, Actions } from './$types';
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

export const actions: Actions = {
    default: async ({ request, params, fetch, cookies, url }) => {
        const id = params.id;
        const form = await request.formData();

        const fd = new FormData();
        const fields = ['name','slug','instructor','provider','url','description','keywords','skills','status'];
        for (const f of fields) {
            const v = form.get(f);
            if (v !== null) fd.append(f, String(v));
        }
        const img = form.get('image') || form.get('course_img');
        if (img && typeof img !== 'string') fd.append('image', img as Blob);

        const apiUrl = `http://localhost:8000/api/v1/educator/courses/${id}/update/`;
        const res = await fetch(apiUrl, { method: 'PUT', body: fd });
        if (!res.ok) {
            const text = await res.text().catch(() => '');
            return { success: false, error: `API error ${res.status}: ${text}` };
        }
        return { success: true };
    }
};
