import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

type Source = 'knowledge' | 'analytics' | 'tasks';

@Component({
  selector: 'app-switchboard-indicator',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './switchboard-indicator.component.html',
  styleUrls: ['./switchboard-indicator.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SwitchboardIndicatorComponent {
  @Input() activeSources: Source[] = [];

  isActive(source: Source): boolean {
    return this.activeSources.includes(source);
  }
}
