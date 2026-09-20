/**
 * Global Configuration for FileFlow AI Frontend
 * Reads VITE_API_URL if set in environment (e.g. Vercel dashboard),
 * otherwise defaults to the production Render backend.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_URL || 'https://fileflow-ai-qtmd.onrender.com').replace(/\/$/, '')
