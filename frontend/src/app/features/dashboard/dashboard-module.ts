import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { SharedModule } from '../../shared/shared-module';
import { DashboardRoutingModule } from './dashboard-routing-module';
import { Dashboard } from './pages/dashboard/dashboard';
import { ProjectForm } from './components/project-form/project-form';
import { DeliverableForm } from './components/deliverable-form/deliverable-form';
import { CommentForm } from './components/comment-form/comment-form';

@NgModule({
  declarations: [Dashboard, ProjectForm, DeliverableForm, CommentForm],
  imports: [CommonModule, ReactiveFormsModule, SharedModule, DashboardRoutingModule],
})
export class DashboardModule {}
