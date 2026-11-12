import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { PatientListItem } from '../../models/patient';
import { PatientService } from '../../services/patient.service';

@Component({
  selector: 'app-patient-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './patient-list.component.html',
  styleUrl: './patient-list.component.css',
})
export class PatientListComponent implements OnInit {
  patients: PatientListItem[] = [];
  searchTerm = '';
  loading = false;
  error = '';

  constructor(private patientService: PatientService) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.patientService.list(this.searchTerm.trim() || undefined).subscribe({
      next: (patients) => {
        this.patients = patients;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load patients. Is the backend running?';
        this.loading = false;
      },
    });
  }

  onSearch(): void {
    this.fetch();
  }
}
