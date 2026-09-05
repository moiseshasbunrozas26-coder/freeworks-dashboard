export type ProjectStatus = 'pending' | 'in_progress' | 'completed';
export type ProjectPriority = 'low' | 'medium' | 'high';

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Client {
  id: number;
  name: string;
  company: string;
  email: string;
  project_count: number;
  created_at: string;
}

export interface Deliverable {
  id: number;
  project: number;
  project_name: string;
  name: string;
  description: string;
  due_date: string;
  is_delivered: boolean;
  delivered_at: string | null;
  simulated_file: string;
  is_overdue: boolean;
  created_at: string;
}

export interface ClientComment {
  id: number;
  project: number;
  project_name: string;
  author: string;
  content: string;
  created_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  client: Client;
  start_date: string;
  due_date: string;
  status: ProjectStatus;
  status_label: string;
  priority: ProjectPriority;
  priority_label: string;
  manual_progress: number | null;
  calculated_progress: number;
  progress_percentage: number;
  display_status: string;
  is_overdue: boolean;
  deliverables: Deliverable[];
  comments: ClientComment[];
  created_at: string;
  updated_at: string;
}

export interface ProjectFormData {
  name: string;
  description: string;
  client_id: number;
  start_date: string;
  due_date: string;
  status: ProjectStatus;
  priority: ProjectPriority;
  manual_progress: number | null;
}

export interface DeliverableFormData {
  project: number;
  name: string;
  description: string;
  due_date: string;
  is_delivered: boolean;
  delivered_at: string | null;
  simulated_file: string;
}

export interface CommentFormData {
  project: number;
  author: string;
  content: string;
}

export interface ProjectFilters {
  client?: number | null;
  status?: ProjectStatus | 'overdue' | '';
  priority?: ProjectPriority | '';
  search?: string;
}

export interface DashboardStatistics {
  total_projects: number;
  pending_projects: number;
  in_progress_projects: number;
  completed_projects: number;
  overdue_projects: number;
  average_progress: number;
  total_deliverables: number;
  delivered_deliverables: number;
}

export interface OverdueNotification {
  id: number;
  type: 'overdue_delivery';
  message: string;
  project_id: number;
  project_name: string;
  client_name: string;
  deliverable_name: string;
  due_date: string;
  days_overdue: number;
}

export interface NotificationResponse {
  count: number;
  results: OverdueNotification[];
}