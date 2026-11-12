import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Encounter } from '../../models/encounter';
import { EncounterService } from '../../services/encounter.service';

const EMPTY: Encounter = {
  visit_date: new Date().toISOString().slice(0, 10),
  bp_systolic: null,
  bp_diastolic: null,
  heart_rate: null,
  temperature_c: null,
  weight_kg: null,
  chief_complaint: '',
  symptoms: '',
  examination_notes: '',
  assessment: '',
  plan: '',
};

@Component({
  selector: 'app-encounter-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './encounter-form.component.html',
})
export class EncounterFormComponent {
  @Input({ required: true }) patientId!: number;
  @Output() saved = new EventEmitter<Encounter>();

  encounter: Encounter = { ...EMPTY };
  error = '';
  saving = false;

  constructor(private encounterService: EncounterService) {}

  submit(): void {
    if (!this.encounter.visit_date) {
      this.error = 'Visit date is required.';
      return;
    }
    this.saving = true;
    this.encounterService.create(this.patientId, this.encounter).subscribe({
      next: (created) => {
        this.saved.emit(created);
        this.encounter = { ...EMPTY, visit_date: new Date().toISOString().slice(0, 10) };
        this.error = '';
        this.saving = false;
      },
      error: () => {
        this.error = 'Failed to save encounter.';
        this.saving = false;
      },
    });
  }
}
