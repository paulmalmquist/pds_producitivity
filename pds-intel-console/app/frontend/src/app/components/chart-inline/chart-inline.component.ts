import { AfterViewInit, ChangeDetectionStrategy, Component, ElementRef, Input, OnChanges, OnDestroy, SimpleChanges, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Chart, ChartConfiguration } from 'chart.js/auto';

@Component({
  selector: 'app-chart-inline',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chart-inline.component.html',
  styleUrls: ['./chart-inline.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ChartInlineComponent implements AfterViewInit, OnChanges, OnDestroy {
  @Input() config?: ChartConfiguration;
  @ViewChild('canvas', { static: true }) canvas!: ElementRef<HTMLCanvasElement>;

  private chart?: Chart;

  ngAfterViewInit(): void {
    this.render();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['config'] && this.chart) {
      this.render(true);
    }
  }

  ngOnDestroy(): void {
    this.chart?.destroy();
  }

  private render(update = false): void {
    if (!this.canvas || !this.config) {
      return;
    }

    if (update && this.chart) {
      this.chart.config = this.config;
      this.chart.update();
      return;
    }

    this.chart?.destroy();
    this.chart = new Chart(this.canvas.nativeElement, this.config);
  }
}
