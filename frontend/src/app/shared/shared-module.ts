import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatCard } from './components/stat-card/stat-card';
import { ProjectCard } from './components/project-card/project-card';
import { NotificationPanel } from './components/notification-panel/notification-panel';

@NgModule({
  declarations: [StatCard, ProjectCard, NotificationPanel],
  imports: [CommonModule],
  exports: [StatCard, ProjectCard, NotificationPanel],
})
export class SharedModule {}
