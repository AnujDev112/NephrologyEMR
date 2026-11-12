import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'patients' },
  {
    path: 'patients',
    loadComponent: () =>
      import('./components/patient-list/patient-list.component').then(
        (m) => m.PatientListComponent
      ),
  },
  {
    path: 'patients/new',
    loadComponent: () =>
      import('./components/patient-form/patient-form.component').then(
        (m) => m.PatientFormComponent
      ),
  },
  {
    path: 'patients/:id',
    loadComponent: () =>
      import('./components/patient-detail/patient-detail.component').then(
        (m) => m.PatientDetailComponent
      ),
  },
];
