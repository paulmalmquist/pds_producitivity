import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SwitchboardIndicatorComponent } from './components/switchboard-indicator/switchboard-indicator.component';
import { RouterService, Source } from './services/router.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SwitchboardIndicatorComponent],
  template: `
    <div class="app-shell">
      <header>
        <h1>JLL PDS Intel Console</h1>
        <app-switchboard-indicator
          [activeSources]="activeSources()"
        ></app-switchboard-indicator>
      </header>
      <main>
        <router-outlet></router-outlet>
      </main>
      <footer>
        <span>JLL Project &amp; Development Services</span>
      </footer>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {
  readonly activeSources = signal<Source[]>(this.routerService.activeSourcesSignal());

  constructor(private readonly routerService: RouterService) {
    this.routerService.activeSourcesChanged.subscribe((sources) =>
      this.activeSources.set(sources)
    );
  }
}
