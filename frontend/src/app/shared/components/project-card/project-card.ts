import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  Project,
  ProjectStatus
} from '../../../core/models/freeworks.models';

@Component({
  selector: 'app-project-card',
  templateUrl: './project-card.html',
  standalone: false,
  styleUrl: './project-card.scss'
})
export class ProjectCard {
  @Input({ required: true }) project!: Project;

  @Output() viewProject = new EventEmitter<Project>();
  @Output() editProject = new EventEmitter<Project>();
  @Output() deleteProject = new EventEmitter<Project>();
  @Output() addDeliverable = new EventEmitter<Project>();
  @Output() statusChange = new EventEmitter<ProjectStatus>();
  @Output() progressChange = new EventEmitter<number>();

  onStatusChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    this.statusChange.emit(select.value as ProjectStatus);
  }

  onProgressChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.progressChange.emit(Number(input.value));
  }

  get deliveredCount(): number {
    return this.project.deliverables.filter(
      deliverable => deliverable.is_delivered
    ).length;
  }

  get statusClass(): string {
    if (this.project.is_overdue) {
      return 'overdue';
    }

    return this.project.status;
  }
}