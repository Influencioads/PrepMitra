import type { ReactNode } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button, type ButtonVariant } from './Button';

export interface ModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Renders as a bottom sheet on small screens. */
  sheetOnMobile?: boolean;
}

const sizes = { sm: 'sm:max-w-sm', md: 'sm:max-w-lg', lg: 'sm:max-w-2xl', xl: 'sm:max-w-4xl' };

/** Accessible dialog (Radix primitives, shadcn/ui-style). Handles focus trap, Esc and scroll lock. */
export function Modal({ open, onOpenChange, title, description, children, footer, size = 'md', sheetOnMobile = true }: ModalProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-stone-900/50 backdrop-blur-[1px] animate-fade-in" />
        <Dialog.Content
          className={cn(
            'fixed z-50 flex max-h-[90vh] w-full flex-col bg-card shadow-overlay animate-fade-in focus:outline-none',
            sheetOnMobile
              ? 'inset-x-0 bottom-0 rounded-t-2xl sm:inset-auto sm:left-1/2 sm:top-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2 sm:rounded-2xl'
              : 'left-1/2 top-1/2 w-[calc(100%-2rem)] -translate-x-1/2 -translate-y-1/2 rounded-2xl',
            sizes[size],
          )}
        >
          <div className="flex items-start justify-between gap-4 border-b border-line px-5 py-4">
            <div>
              <Dialog.Title className="text-lg font-semibold text-ink">{title}</Dialog.Title>
              {description ? (
                <Dialog.Description className="mt-1 text-sm text-muted">{description}</Dialog.Description>
              ) : (
                <Dialog.Description className="sr-only">{typeof title === 'string' ? title : 'Dialog'}</Dialog.Description>
              )}
            </div>
            <Dialog.Close className="rounded-md p-1 text-muted hover:bg-stone-100 hover:text-ink" aria-label="Close dialog">
              <X className="h-5 w-5" />
            </Dialog.Close>
          </div>
          {children && <div className="overflow-y-auto px-5 py-4 scrollbar-thin">{children}</div>}
          {footer && <div className="flex flex-col-reverse gap-2 border-t border-line px-5 py-4 sm:flex-row sm:justify-end">{footer}</div>}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

export interface ConfirmationDialogProps {
  size?: 'sm' | 'md' | 'lg';
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void | Promise<void>;
  variant?: ButtonVariant;
  loading?: boolean;
  children?: ReactNode;
}

export function ConfirmationDialog({
  open, onOpenChange, title, description, confirmLabel = 'Confirm', cancelLabel = 'Cancel', onConfirm, variant = 'primary', loading, children, size = 'sm',
}: ConfirmationDialogProps) {
  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title={title}
      description={description}
      size={size}
      footer={
        <>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
            {cancelLabel}
          </Button>
          <Button variant={variant} onClick={() => void onConfirm()} loading={loading}>
            {confirmLabel}
          </Button>
        </>
      }
    >
      {children}
    </Modal>
  );
}
