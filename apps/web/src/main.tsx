import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/styles/index.css';
import { App } from '@/app/App';
import { setExamCatalogSource, setRoleSource } from '@/services';
import { getAdminExams, getAdminRoles } from '@/store/adminStore';
import { registerSW } from '@/pwa/registerSW';

// Learner catalog reads exams/roles managed in the admin console (demo stand-in for /v1/exams and /v1/interview-roles).
setExamCatalogSource(getAdminExams);
setRoleSource(getAdminRoles);

registerSW();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
