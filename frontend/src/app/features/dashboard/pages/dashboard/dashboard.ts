import {
  ChangeDetectorRef,
  Component,
  DestroyRef,
  OnInit,
  inject
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder } from '@angular/forms';
import { forkJoin } from 'rxjs';
import {
  debounceTime,
  distinctUntilChanged
} from 'rxjs/operators';

import {
  Client,
  DashboardStatistics,
  OverdueNotification,
  Project,
  ProjectFilters,
  ProjectFormData,
  ProjectStatus
} from '../../../../core/models/freeworks.models';
import {
  FreeworksApiService
} from '../../../../core/services/freeworks-api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  standalone: false,
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  private readonly api = inject(FreeworksApiService);
  private readonly formBuilder = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly changeDetector = inject(ChangeDetectorRef);

  readonly filtersForm = this.formBuilder.group({
    search: [''],
    client: [''],
    status: [''],
    priority: ['']
  });

  clients: Client[] = [];
  projects: Project[] = [];
  notifications: OverdueNotification[] = [];

  statistics: DashboardStatistics = {
    total_projects: 0,
    pending_projects: 0,
    in_progress_projects: 0,
    completed_projects: 0,
    overdue_projects: 0,
    average_progress: 0,
    total_deliverables: 0,
    delivered_deliverables: 0
  };

  loading = true;
  errorMessage = '';
  successMessage = '';

  selectedProject: Project | null = null;

  projectFormOpen = false;
  editingProject: Project | null = null;
  submittingProject = false;

  ngOnInit(): void {
    this.loadDashboard();

    this.filtersForm.valueChanges
      .pipe(
        debounceTime(350),
        distinctUntilChanged(
          (previous, current) =>
            JSON.stringify(previous) === JSON.stringify(current)
        ),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe(() => this.loadProjectsAndStatistics());
  }

  loadDashboard(): void {
    this.loading = true;
    this.errorMessage = '';

    forkJoin({
      clients: this.api.getClients(),
      projects: this.api.getProjects(this.currentFilters),
      statistics: this.api.getStatistics(this.currentFilters),
      notifications: this.api.getNotifications()
    }).subscribe({
      next: result => {
        this.clients = result.clients.results;
        this.projects = result.projects.results;
        this.statistics = result.statistics;
        this.notifications = result.notifications.results;
        this.loading = false;
        this.changeDetector.detectChanges();
      },
      error: () => {
        this.errorMessage =
          'No fue posible conectar con el servidor. Verifica que Django esté iniciado.';
        this.loading = false;
        this.changeDetector.detectChanges();
      }
    });
  }

  loadProjectsAndStatistics(): void {
    this.loading = true;
    this.errorMessage = '';

    forkJoin({
      projects: this.api.getProjects(this.currentFilters),
      statistics: this.api.getStatistics(this.currentFilters)
    }).subscribe({
      next: result => {
        this.projects = result.projects.results;
        this.statistics = result.statistics;
        this.loading = false;
        this.changeDetector.detectChanges();
      },
      error: () => {
        this.errorMessage = 'No fue posible aplicar los filtros.';
        this.loading = false;
        this.changeDetector.detectChanges();
      }
    });
  }

  clearFilters(): void {
    this.filtersForm.reset({
      search: '',
      client: '',
      status: '',
      priority: ''
    });
  }

  openCreateProject(): void {
    this.editingProject = null;
    this.projectFormOpen = true;
  }

  editProject(project: Project): void {
    this.editingProject = project;
    this.projectFormOpen = true;
  }

  closeProjectForm(): void {
    if (this.submittingProject) {
      return;
    }

    this.projectFormOpen = false;
    this.editingProject = null;
  }

  saveProject(data: ProjectFormData): void {
    this.submittingProject = true;
    this.errorMessage = '';

    const request = this.editingProject
      ? this.api.updateProject(this.editingProject.id, data)
      : this.api.createProject(data);

    request.subscribe({
      next: () => {
        const message = this.editingProject
          ? 'Proyecto actualizado correctamente.'
          : 'Proyecto creado correctamente.';

        this.submittingProject = false;
        this.projectFormOpen = false;
        this.editingProject = null;

        this.showSuccess(message);
        this.loadDashboard();
      },
      error: error => {
        this.submittingProject = false;

        if (error?.error?.due_date) {
          this.errorMessage = error.error.due_date[0];
        } else if (error?.error?.name) {
          this.errorMessage = error.error.name[0];
        } else {
          this.errorMessage =
            'No fue posible guardar el proyecto. Revisa los datos ingresados.';
        }

        this.changeDetector.detectChanges();
      }
    });
  }

  changeStatus(
    project: Project,
    projectStatus: ProjectStatus
  ): void {
    this.api.updateStatus(project.id, projectStatus).subscribe({
      next: () => {
        this.showSuccess('Estado actualizado correctamente.');
        this.loadDashboard();
      },
      error: () => {
        this.errorMessage = 'No fue posible actualizar el estado.';
        this.changeDetector.detectChanges();
      }
    });
  }

  changeProgress(project: Project, progress: number): void {
    this.api.updateProgress(project.id, progress).subscribe({
      next: () => {
        this.showSuccess('Progreso actualizado correctamente.');
        this.loadProjectsAndStatistics();
      },
      error: () => {
        this.errorMessage = 'No fue posible actualizar el progreso.';
        this.changeDetector.detectChanges();
      }
    });
  }

  removeProject(project: Project): void {
    const confirmed = window.confirm(
      `¿Deseas eliminar el proyecto "${project.name}"?`
    );

    if (!confirmed) {
      return;
    }

    this.api.deleteProject(project.id).subscribe({
      next: () => {
        this.showSuccess('Proyecto eliminado correctamente.');
        this.loadDashboard();
      },
      error: () => {
        this.errorMessage = 'No fue posible eliminar el proyecto.';
        this.changeDetector.detectChanges();
      }
    });
  }

  openProject(project: Project): void {
    this.selectedProject = project;
  }

  openProjectById(projectId: number): void {
    this.api.getProject(projectId).subscribe({
      next: project => {
        this.selectedProject = project;
        this.changeDetector.detectChanges();
      },
      error: () => {
        this.errorMessage = 'No fue posible cargar el proyecto.';
        this.changeDetector.detectChanges();
      }
    });
  }

  closeProject(): void {
    this.selectedProject = null;
  }

  addDeliverable(project: Project): void {
    this.selectedProject = project;
    this.showSuccess(
      `Proyecto "${project.name}" seleccionado para agregar un entregable.`
    );
  }

  trackProject(_: number, project: Project): number {
    return project.id;
  }

  private get currentFilters(): ProjectFilters {
    const values = this.filtersForm.getRawValue();

    return {
      search: values.search ?? '',
      client: values.client ? Number(values.client) : null,
      status: (
        values.status ?? ''
      ) as ProjectFilters['status'],
      priority: (
        values.priority ?? ''
      ) as ProjectFilters['priority']
    };
  }

  private showSuccess(message: string): void {
    this.successMessage = message;
    this.changeDetector.detectChanges();

    window.setTimeout(() => {
      this.successMessage = '';
      this.changeDetector.detectChanges();
    }, 3000);
  }
}