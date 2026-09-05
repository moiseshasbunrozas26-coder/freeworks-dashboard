import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-stat-card',
  templateUrl: './stat-card.html',
  standalone: false,
  styleUrl: './stat-card.scss'
})
export class StatCard {
  @Input() label = '';
  @Input() value: string | number = 0;
  @Input() subtitle = '';
  @Input() icon = '📊';
  @Input() tone: 'blue' | 'green' | 'orange' | 'red' = 'blue';
}