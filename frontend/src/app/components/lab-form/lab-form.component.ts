import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LabResult } from '../../models/lab-result';
import { LabService } from '../../services/lab.service';

const EMPTY: LabResult = {
  test_date: new Date().toISOString().slice(0, 10),
  serum_creatinine: null,
  egfr: null,
  bun: null,
  potassium: null,
  hemoglobin: null,
  calcium: null,
  phosphorus: null,
  uacr: null,
};

@Component({
  selector: 'app-lab-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lab-form.component.html',
})
export class LabFormComponent {
  @Input({ required: true }) patientId!: number;
  @Output() saved = new EventEmitter<LabResult>();

  lab: LabResult = { ...EMPTY };
  error = '';
  saving = false;

  constructor(private labService: LabService) {}

  submit(): void {
    if (!this.lab.test_date) {
      this.error = 'Test date is required.';
      return;
    }
    this.saving = true;
    this.labService.create(this.patientId, this.lab).subscribe({
      next: (created) => {
        this.saved.emit(created);
        this.lab = { ...EMPTY, test_date: new Date().toISOString().slice(0, 10) };
        this.error = '';
        this.saving = false;
      },
      error: () => {
        this.error = 'Failed to save lab result.';
        this.saving = false;
      },
    });
  }
}
