import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { AISummaryResponse } from '../../models/ai-summary';
import { AiService } from '../../services/ai.service';

@Component({
  selector: 'app-ai-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ai-summary.component.html',
})
export class AiSummaryComponent {
  @Input({ required: true }) patientId!: number;

  result: AISummaryResponse | null = null;
  loading = false;
  error = '';

  constructor(private aiService: AiService) {}

  generate(): void {
    this.loading = true;
    this.error = '';
    this.result = null;
    this.aiService.generateSummary(this.patientId).subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: (err) => {
        this.error =
          err?.error?.detail || 'Failed to generate AI summary. Please try again later.';
        this.loading = false;
      },
    });
  }
}
