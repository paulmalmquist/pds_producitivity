import { ChangeDetectionStrategy, Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlaybookService } from '../../services/playbook.service';

@Component({
  selector: 'app-playbooks-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './playbooks.page.html',
  styleUrls: ['./playbooks.page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlaybooksPageComponent implements OnInit {
  readonly playbooks = signal<{ name: string; steps: string[] }[]>([]);

  constructor(private readonly playbookService: PlaybookService) {}

  ngOnInit(): void {
    this.playbookService.getPlaybooks().subscribe((playbooks) =>
      this.playbooks.set(playbooks)
    );
  }
}
