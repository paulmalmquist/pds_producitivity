import { ChangeDetectionStrategy, Component, Input, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartCardComponent } from '../chart-card/chart-card.component';

export interface DeckCard {
  type: 'project' | 'vendor' | 'person' | 'metric' | 'chart';
  title: string;
  description: string;
  actions?: string[];
  chartConfig?: unknown;
}

@Component({
  selector: 'app-context-deck',
  standalone: true,
  imports: [CommonModule, ChartCardComponent],
  templateUrl: './context-deck.component.html',
  styleUrls: ['./context-deck.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ContextDeckComponent {
  @Input() set cards(value: DeckCard[]) {
    this._cards.set(value);
  }

  readonly _cards = signal<DeckCard[]>([]);
}
