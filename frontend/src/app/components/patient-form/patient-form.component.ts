import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PatientCreate } from '../../models/patient';
import { PatientService } from '../../services/patient.service';

@Component({
  selector: 'app-patient-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './patient-form.component.html',
})
export class PatientFormComponent {
  patient: PatientCreate = {
    name: '',
    date_of_birth: '',
    gender: 'Female',
    primary_diagnosis: '',
    contact_number: '',
    medical_history: '',
  };
  error = '';
  saving = false;

  constructor(private patientService: PatientService, private router: Router) {}

  submit(): void {
    if (!this.patient.name || !this.patient.date_of_birth) {
      this.error = 'Name and date of birth are required.';
      return;
    }
    this.saving = true;
    this.patientService.create(this.patient).subscribe({
      next: (created) => this.router.navigate(['/patients', created.id]),
      error: () => {
        this.error = 'Failed to create patient.';
        this.saving = false;
      },
    });
  }
}
