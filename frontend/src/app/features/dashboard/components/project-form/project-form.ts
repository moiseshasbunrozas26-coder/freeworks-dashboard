import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  inject
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  ValidationErrors,
  Validators
} from '@angular/forms';

import {
  Client,
  Project,
  ProjectFormData,
  ProjectPriority,
  ProjectStatus
} from '../../../../core/models/freeworks.models';

function dateRangeValidator(
  control: AbstractControl
): ValidationErrors | null {
  const startDate = control.get('startDate')?.value;
  const dueDate = control.get('dueDate')?.value;

  if (startDate && dueDate && dueDate < startDate) {
    return { invalidDateRange: true };
  }

  return null;
}

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.html',
  standalone: false,
  styleUrl: './project-form.scss'
})
export class ProjectForm implements OnChanges {
  private readonly formBuilder = inject(FormBuilder);

  @Input() clients: Client[] = [];
  @Input() project: Project | null = null;
  @Input() submitting = false;

  @Output() saveProject = new EventEmitter<ProjectFormData>();
  @Output() cancelForm = new EventEmitter<void>();

  readonly form = this.formBuilder.group(
    {
      name: [
        '',
        [
          Validators.required,
          Validators.minLength(3),
          Validators.maxLength(150)
        ]
      ],
      description: [
        '',
        [Validators.maxLength(1000)]
      ],
      clientId: [
        '',
        [Validators.required]
      ],
      startDate: [
        '',
        [Validators.required]
      ],
      dueDate: [
        '',
        [Validators.required]
      ],
      status: [
        'pending',
        [Validators.required]
      ],
      priority: [
        'medium',
        [Validators.required]
      ],
      manualProgress: [
        null as number | null,
        [
          Validators.min(0),
          Validators.max(100)
        ]
      ]
    },
    {
      validators: dateRangeValidator
    }
  );

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes['project']) {
      return;
    }

    if (this.project) {
      this.form.reset({
        name: this.project.name,
        description: this.project.description,
        clientId: this.project.client.id.toString(),
        startDate: this.project.start_date,
        dueDate: this.project.due_date,
        status: this.project.status,
        priority: this.project.priority,
        manualProgress: this.project.manual_progress
      });
    } else {
      this.form.reset({
        name: '',
        description: '',
        clientId: '',
        startDate: '',
        dueDate: '',
        status: 'pending',
        priority: 'medium',
        manualProgress: null
      });
    }
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const values = this.form.getRawValue();

    this.saveProject.emit({
      name: values.name?.trim() ?? '',
      description: values.description?.trim() ?? '',
      client_id: Number(values.clientId),
      start_date: values.startDate ?? '',
      due_date: values.dueDate ?? '',
      status: values.status as ProjectStatus,
      priority: values.priority as ProjectPriority,
      manual_progress: values.manualProgress
    });
  }

  isInvalid(fieldName: string): boolean {
    const field = this.form.get(fieldName);
    return Boolean(field?.invalid && field.touched);
  }
}