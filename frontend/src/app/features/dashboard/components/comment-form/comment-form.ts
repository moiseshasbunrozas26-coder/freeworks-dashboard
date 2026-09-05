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
  FormBuilder,
  Validators
} from '@angular/forms';

import {
  CommentFormData,
  Project
} from '../../../../core/models/freeworks.models';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.html',
  standalone: false,
  styleUrl: './comment-form.scss'
})
export class CommentForm implements OnChanges {
  private readonly formBuilder = inject(FormBuilder);

  @Input() project: Project | null = null;
  @Input() submitting = false;

  @Output() saveComment = new EventEmitter<CommentFormData>();

  readonly form = this.formBuilder.group({
    author: [
      'Cliente',
      [
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(120)
      ]
    ],
    content: [
      '',
      [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(2000)
      ]
    ]
  });

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['project']) {
      this.form.reset({
        author: 'Cliente',
        content: ''
      });
    }
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

    this.saveComment.emit({
      project: this.project.id,
      author: values.author?.trim() ?? '',
      content: values.content?.trim() ?? ''
    });
  }

  clearAfterSave(): void {
    this.form.reset({
      author: 'Cliente',
      content: ''
    });
  }

  isInvalid(fieldName: string): boolean {
    const field = this.form.get(fieldName);
    return Boolean(field?.invalid && field.touched);
  }
}