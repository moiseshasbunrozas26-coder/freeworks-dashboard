import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  Client,
  ClientComment,
  CommentFormData,
  DashboardStatistics,
  Deliverable,
  DeliverableFormData,
  NotificationResponse,
  PaginatedResponse,
  Project,
  ProjectFilters,
  ProjectFormData,
  ProjectStatus
} from '../models/freeworks.models';

@Injectable({
  providedIn: 'root'
})
export class FreeworksApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api';

  getClients(search = ''): Observable<PaginatedResponse<Client>> {
    let params = new HttpParams();

    if (search.trim()) {
      params = params.set('search', search.trim());
    }

    return this.http.get<PaginatedResponse<Client>>(
      `${this.apiUrl}/clients/`,
      { params }
    );
  }

  getProjects(
    filters: ProjectFilters = {}
  ): Observable<PaginatedResponse<Project>> {
    return this.http.get<PaginatedResponse<Project>>(
      `${this.apiUrl}/projects/`,
      { params: this.buildProjectParams(filters) }
    );
  }

  getProject(id: number): Observable<Project> {
    return this.http.get<Project>(
      `${this.apiUrl}/projects/${id}/`
    );
  }

  createProject(data: ProjectFormData): Observable<Project> {
    return this.http.post<Project>(
      `${this.apiUrl}/projects/`,
      data
    );
  }

  updateProject(
    id: number,
    data: Partial<ProjectFormData>
  ): Observable<Project> {
    return this.http.patch<Project>(
      `${this.apiUrl}/projects/${id}/`,
      data
    );
  }

  deleteProject(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/projects/${id}/`
    );
  }

  updateProgress(
    id: number,
    manualProgress: number | null
  ): Observable<Project> {
    return this.http.patch<Project>(
      `${this.apiUrl}/projects/${id}/progress/`,
      { manual_progress: manualProgress }
    );
  }

  updateStatus(
    id: number,
    projectStatus: ProjectStatus
  ): Observable<Project> {
    return this.http.patch<Project>(
      `${this.apiUrl}/projects/${id}/status/`,
      { status: projectStatus }
    );
  }

  getStatistics(
    filters: ProjectFilters = {}
  ): Observable<DashboardStatistics> {
    return this.http.get<DashboardStatistics>(
      `${this.apiUrl}/projects/statistics/`,
      { params: this.buildProjectParams(filters) }
    );
  }

  getNotifications(): Observable<NotificationResponse> {
    return this.http.get<NotificationResponse>(
      `${this.apiUrl}/projects/notifications/`
    );
  }

  getDeliverables(
    projectId?: number
  ): Observable<PaginatedResponse<Deliverable>> {
    let params = new HttpParams();

    if (projectId !== undefined) {
      params = params.set('project', projectId.toString());
    }

    return this.http.get<PaginatedResponse<Deliverable>>(
      `${this.apiUrl}/deliverables/`,
      { params }
    );
  }

  createDeliverable(
    data: DeliverableFormData
  ): Observable<Deliverable> {
    return this.http.post<Deliverable>(
      `${this.apiUrl}/deliverables/`,
      data
    );
  }

  updateDeliverable(
    id: number,
    data: Partial<DeliverableFormData>
  ): Observable<Deliverable> {
    return this.http.patch<Deliverable>(
      `${this.apiUrl}/deliverables/${id}/`,
      data
    );
  }

  deleteDeliverable(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/deliverables/${id}/`
    );
  }

  getComments(
    projectId?: number
  ): Observable<PaginatedResponse<ClientComment>> {
    let params = new HttpParams();

    if (projectId !== undefined) {
      params = params.set('project', projectId.toString());
    }

    return this.http.get<PaginatedResponse<ClientComment>>(
      `${this.apiUrl}/comments/`,
      { params }
    );
  }

  createComment(
    data: CommentFormData
  ): Observable<ClientComment> {
    return this.http.post<ClientComment>(
      `${this.apiUrl}/comments/`,
      data
    );
  }

  deleteComment(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/comments/${id}/`
    );
  }

  private buildProjectParams(filters: ProjectFilters): HttpParams {
    let params = new HttpParams();

    if (filters.client !== undefined && filters.client !== null) {
      params = params.set('client', filters.client.toString());
    }

    if (filters.status) {
      params = params.set('status', filters.status);
    }

    if (filters.priority) {
      params = params.set('priority', filters.priority);
    }

    if (filters.search?.trim()) {
      params = params.set('search', filters.search.trim());
    }

    return params;
  }
}