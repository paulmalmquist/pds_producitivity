import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeckCard } from '../context-deck/context-deck.component';
import { ChartInlineComponent } from '../chart-inline/chart-inline.component';

@Component({
  selector: 'app-chart-card',
  standalone: true,
  imports: [CommonModule, ChartInlineComponent],
  templateUrl: './chart-card.component.html',
  styleUrls: ['./chart-card.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ChartCardComponent {
  @Input({ required: true }) card!: DeckCard;
  @Output() changeType = new EventEmitter<void>();
  @Output() pin = new EventEmitter<void>();
  @Output() createJira = new EventEmitter<void>();
  @Output() openTableau = new EventEmitter<void>();
}
