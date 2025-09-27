import { ChangeDetectionStrategy, Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AiChatPaneComponent } from '../../components/ai-chat-pane/ai-chat-pane.component';
import { ContextDeckComponent, DeckCard } from '../../components/context-deck/context-deck.component';
import { WorkspaceStateService } from '../../state/workspace-state.service';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule, AiChatPaneComponent, ContextDeckComponent],
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomePageComponent implements OnInit {
  readonly workspaceCards = signal<DeckCard[]>([]);
  readonly lastChats = computed(() => this.workspaceState.lastChats());

  constructor(private readonly workspaceState: WorkspaceStateService) {}

  ngOnInit(): void {
    this.workspaceCards.set(this.workspaceState.pinnedCards());
  }
}
