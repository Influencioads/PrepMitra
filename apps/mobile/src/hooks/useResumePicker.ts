import { useState } from 'react';
import * as DocumentPicker from 'expo-document-picker';
import type { ResumeInfo } from '@prepmitra/shared';
import { RESUME_RULES, validateResumeFile } from '@prepmitra/shared';
import { errorMessage, profileService } from '@/services';

/**
 * Picks a resume with the system document picker, validates it with the shared
 * rules (PDF/DOCX, ≤ 5 MB) and runs the simulated upload.
 */
export function useResumePicker(onPicked?: (r: ResumeInfo) => void) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const pick = async (): Promise<ResumeInfo | null> => {
    setError(null);
    let result: DocumentPicker.DocumentPickerResult;
    try {
      result = await DocumentPicker.getDocumentAsync({
        type: [...RESUME_RULES.acceptedMimeTypes],
        copyToCacheDirectory: true,
        multiple: false,
      });
    } catch (e) {
      setError(errorMessage(e, 'Could not open the file picker.'));
      return null;
    }
    if (result.canceled || !result.assets[0]) return null;
    const asset = result.assets[0];
    const file = { uri: asset.uri, name: asset.name, size: asset.size ?? 0, mimeType: asset.mimeType };
    const check = validateResumeFile({ name: file.name, size: file.size, type: file.mimeType });
    if (!check.ok) {
      setError(check.error);
      return null;
    }
    setUploading(true);
    try {
      const info = await profileService.uploadResume(file);
      onPicked?.(info);
      return info;
    } catch (e) {
      setError(errorMessage(e));
      return null;
    } finally {
      setUploading(false);
    }
  };

  return { pick, uploading, error, clearError: () => setError(null) };
}
