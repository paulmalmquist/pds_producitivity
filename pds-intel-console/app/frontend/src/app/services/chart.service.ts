import { Injectable } from '@angular/core';
import { ChartConfiguration } from 'chart.js/auto';

export interface ChartInputs {
  columns: string[];
  rows: (string | number)[][];
  viz_hints?: {
    chartType?: string;
    x?: string;
    y?: string;
    series?: string;
    isTimeSeries?: boolean;
    percentLike?: boolean;
  };
}

@Injectable({ providedIn: 'root' })
export class ChartService {
  buildChart(config: ChartInputs): ChartConfiguration {
    const { columns, rows, viz_hints } = config;
    const { chartType, horizontal } = this.resolveChartType(columns, rows, viz_hints);
    const categoryColumn = viz_hints?.x ?? columns[0];
    const valueColumn = viz_hints?.y ?? columns[1] ?? columns[0];
    const labels = rows.map((row) => String(row[columns.indexOf(categoryColumn)] ?? row[0]));
    const data = rows.map((row) => Number(row[columns.indexOf(valueColumn)] ?? row[1] ?? 0));

    const dataset = {
      label: viz_hints?.y ?? valueColumn,
      data,
      backgroundColor: '#da291c',
      borderColor: '#da291c',
      fill: chartType === 'line' ? false : true
    };

    const configuration: ChartConfiguration = {
      type: chartType as ChartConfiguration['type'],
      data: {
        labels,
        datasets: [dataset]
      },
      options: {
        responsive: true,
        indexAxis: horizontal ? 'y' : 'x',
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
          }
        },
        scales:
          chartType === 'pie' || chartType === 'doughnut'
            ? {}
            : {
                x: {
                  ticks: {
                    autoSkip: true
                  }
                },
                y: {
                  beginAtZero: true
                }
              }
      }
    };

    return configuration;
  }

  private resolveChartType(
    columns: string[],
    rows: (string | number)[][],
    viz_hints?: ChartInputs['viz_hints']
  ): { chartType: string; horizontal: boolean } {
    if (viz_hints?.chartType) {
      if (viz_hints.chartType.toLowerCase() === 'horizontalbar') {
        return { chartType: 'bar', horizontal: true };
      }
      return { chartType: viz_hints.chartType, horizontal: false };
    }

    if (viz_hints?.isTimeSeries) {
      return { chartType: 'line', horizontal: false };
    }

    const categoricalCount = rows.length;
    const values = rows.map((row) => Number(row[columns.indexOf(viz_hints?.y ?? columns[1] ?? columns[0])] ?? 0));
    const total = values.reduce((acc, val) => acc + val, 0);
    const percentLike = viz_hints?.percentLike ?? (Math.abs(total - 100) < 5 && total !== 0);

    if (percentLike) {
      return { chartType: 'doughnut', horizontal: false };
    }

    if (categoricalCount < 15) {
      return { chartType: 'bar', horizontal: false };
    }

    return { chartType: 'bar', horizontal: true };
  }
}
