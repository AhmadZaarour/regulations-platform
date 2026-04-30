import { getToken } from "./auth";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

type ApiOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  auth?: boolean;
};

export async function apiFetch<T>(
  path: string,
  options: ApiOptions = {},
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (options.auth) {
    const token = getToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type RunCreateResponse = {
  run_id: number;
  job_id: string;
  status: string;
};

export type RunResultResponse = {
  id: number;
  status: string;
  project_type: string;
  input_data: Record<string, unknown>;
  result: Record<string, unknown> | null;
  error_message: string | null;
  rq_job_id: string | null;
  created_at: string | null;
  started_at: string | null;
  finished_at: string | null;
};

export type RunListItem = {
  id: number;
  status: string;
  project_type: string;
  created_at: string | null;
  finished_at: string | null;
};

export type RunListResponse = {
  items: RunListItem[];
};