import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { forkJoin } from 'rxjs';
import { Encounter } from '../../models/encounter';
import { LabField, LAB_FIELD_LABELS, LabResult, ReferenceRange } from '../../models/lab-result';
import { PatientDetail } from '../../models/patient';
import { EncounterService } from '../../services/encounter.service';
import { LabService } from '../../services/lab.service';
import { PatientService } from '../../services/patient.service';
import { AiSummaryComponent } from '../ai-summary/ai-summary.component';
import { EncounterFormComponent } from '../encounter-form/encounter-form.component';
import { LabChartComponent } from '../lab-chart/lab-chart.component';
import { LabFormComponent } from '../lab-form/lab-form.component';

type Tab = 'overview' | 'encounters' | 'labs' | 'ai';

@Component({
  selector: 'app-patient-detail',
  standalone: true,
  imports: [
    CommonModule,
    EncounterFormComponent,
    LabFormComponent,
    LabChartComponent,
    AiSummaryComponent,
  ],
  templateUrl: './patient-detail.component.html',
})
export class PatientDetailComponent implements OnInit {
  patientId!: number;
  patient: PatientDetail | null = null;
  encounters: Encounter[] = [];
  labs: LabResult[] = [];
  referenceRanges: Record<string, ReferenceRange> = {};
  labFields = Object.keys(LAB_FIELD_LABELS) as LabField[];
  labFieldLabels = LAB_FIELD_LABELS;

  activeTab: Tab = 'overview';
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private patientService: PatientService,
    private encounterService: EncounterService,
    private labService: LabService
  ) {}

  ngOnInit(): void {
    this.patientId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadAll();
  }

  loadAll(): void {
    this.loading = true;
    forkJoin({
      patient: this.patientService.get(this.patientId),
      encounters: this.encounterService.list(this.patientId),
      labs: this.labService.list(this.patientId),
      ranges: this.labService.referenceRanges(),
    }).subscribe({
      next: ({ patient, encounters, labs, ranges }) => {
        this.patient = patient;
        this.encounters = encounters;
        this.labs = labs;
        this.referenceRanges = ranges;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load patient record.';
        this.loading = false;
      },
    });
  }

  setTab(tab: Tab): void {
    this.activeTab = tab;
  }

  onEncounterSaved(encounter: Encounter): void {
    this.encounters = [encounter, ...this.encounters];
  }

  onLabSaved(): void {
    // Re-fetch so the new result comes back with computed CKD stage / flags.
    this.labService.list(this.patientId).subscribe((labs) => (this.labs = labs));
  }

  isAbnormal(lab: LabResult, field: LabField): boolean {
    return !!lab.abnormal_flags?.[field];
  }
}
