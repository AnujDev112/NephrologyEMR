import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges } from '@angular/core';
import { ChartConfiguration } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { LabResult } from '../../models/lab-result';

@Component({
  selector: 'app-lab-chart',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './lab-chart.component.html',
})
export class LabChartComponent implements OnChanges {
  @Input({ required: true }) labs: LabResult[] = [];

  chartData: ChartConfiguration<'line'>['data'] = { labels: [], datasets: [] };
  chartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    interaction: { mode: 'index', intersect: false },
    scales: {
      y: { title: { display: true, text: 'Creatinine (mg/dL)' } },
      y1: {
        position: 'right',
        title: { display: true, text: 'eGFR (mL/min/1.73m²)' },
        grid: { drawOnChartArea: false },
      },
    },
  };

  ngOnChanges(): void {
    // Oldest -> newest for a left-to-right trend line.
    const chronological = [...this.labs].reverse();
    this.chartData = {
      labels: chronological.map((l) => l.test_date),
      datasets: [
        {
          label: 'Serum Creatinine (mg/dL)',
          data: chronological.map((l) => l.serum_creatinine),
          borderColor: '#dc2626',
          yAxisID: 'y',
          spanGaps: true,
        },
        {
          label: 'eGFR (mL/min/1.73m²)',
          data: chronological.map((l) => l.egfr),
          borderColor: '#2563eb',
          yAxisID: 'y1',
          spanGaps: true,
        },
      ],
    };
  }
}
