import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkspaceStateService } from '../../state/workspace-state.service';

@Component({
  selector: 'app-settings-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './settings.page.html',
  styleUrls: ['./settings.page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SettingsPageComponent {
  model = this.workspaceState.settings();

  constructor(private readonly workspaceState: WorkspaceStateService) {}

  save(): void {
    this.workspaceState.updateSettings(this.model);
  }
}
