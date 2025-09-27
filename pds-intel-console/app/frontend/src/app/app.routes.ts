import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home/home.page';
import { SettingsPageComponent } from './pages/settings/settings.page';
import { PlaybooksPageComponent } from './pages/playbooks/playbooks.page';

export const appRoutes: Routes = [
  {
    path: '',
    component: HomePageComponent
  },
  {
    path: 'settings',
    component: SettingsPageComponent
  },
  {
    path: 'playbooks',
    component: PlaybooksPageComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
];
