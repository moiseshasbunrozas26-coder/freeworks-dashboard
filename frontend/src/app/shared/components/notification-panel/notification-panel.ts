import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  OverdueNotification
} from '../../../core/models/freeworks.models';

@Component({
  selector: 'app-notification-panel',
  templateUrl: './notification-panel.html',
  standalone: false,
  styleUrl: './notification-panel.scss'
})
export class NotificationPanel {
  @Input() notifications: OverdueNotification[] = [];
  @Input() loading = false;
  @Output() projectSelected = new EventEmitter<number>();
}