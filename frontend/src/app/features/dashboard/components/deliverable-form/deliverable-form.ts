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
  DeliverableFormData,
  Project
} from '../../../../core/models/freeworks.models';

function deliveryValidator(
  control: AbstractControl
): ValidationErrors | null {
  const isDelivered = control.get('isDelivered')?.value;
  const deliveredAt = control.get('deliveredAt')?.value;

  if (isDelivered && !deliveredAt) {
    return { deliveredDateRequired: true };
  }

  if (!isDelivered && deliveredAt) {
    return { pendingWithDeliveryDate: true };
  }

  return null;
}

@Component({
  selector: 'app-deliverable-form',
  templateUrl: './deliverable-form.html',
  standalone: false,
  styleUrl: './deliverable-form.scss'
})
export class DeliverableForm implements OnChanges {
  private readonly formBuilder = inject(FormBuilder);

  @Input() project: Project | null = null;
  @Input() submitting = false;

  @Output() saveDeliverable =
    new EventEmitter<DeliverableFormData>();

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
        [
          Validators.required,
          Validators.minLength(3),
          Validators.maxLength(1000)
        ]
      ],
      dueDate: [
        '',
        [Validators.required]
      ],
      isDelivered: [false],
      deliveredAt: [null as string | null],
      simulatedFile: [
        '',
        [Validators.maxLength(255)]
      ]
    },
    {
      validators: deliveryValidator
    }
  );

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['project']) {
      this.form.reset({
        name: '',
        description: '',
        dueDate: '',
        isDelivered: false,
        deliveredAt: null,
        simulatedFile: ''
      });
    }
  }

  onDeliveryStateChange(): void {
    const isDelivered =
      this.form.controls.isDelivered.value ?? false;

    if (!isDelivered) {
      this.form.controls.deliveredAt.setValue(null);
    }

    this.form.updateValueAndValidity();
  }

  submit(): void {
    if (!this.project) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const values = this.form.getRawValue();

    this.saveDeliverable.emit({
      project: this.project.id,
      name: values.name?.trim() ?? '',
      description: values.description?.trim() ?? '',
      due_date: values.dueDate ?? '',
      is_delivered: values.isDelivered ?? false,
      delivered_at: values.isDelivered
        ? values.deliveredAt
        : null,
      simulated_file: values.simulatedFile?.trim() ?? ''
    });
  }

  isInvalid(fieldName: string): boolean {
    const field = this.form.get(fieldName);
    return Boolean(field?.invalid && field.touched);
  }
}