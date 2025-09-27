import { ChartService } from './chart.service';

describe('ChartService', () => {
  let service: ChartService;

  beforeEach(() => {
    service = new ChartService();
  });

  it('should use line chart for time series', () => {
    const chart = service.buildChart({
      columns: ['month', 'value'],
      rows: [
        ['2024-01', 100],
        ['2024-02', 120]
      ],
      viz_hints: { isTimeSeries: true, x: 'month', y: 'value' }
    });

    expect(chart.type).toBe('line');
  });

  it('should use horizontal bar for large categorical sets', () => {
    const rows = Array.from({ length: 20 }).map((_, index) => [`Category ${index}`, index]);
    const chart = service.buildChart({ columns: ['label', 'value'], rows });
    expect(chart.options?.indexAxis).toBe('y');
  });
});
