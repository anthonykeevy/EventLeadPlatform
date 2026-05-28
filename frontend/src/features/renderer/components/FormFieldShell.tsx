import React from 'react';
import {
  EDF_FIELD_LIFT_Z_INDEX,
  useEdfFieldLifted,
} from '../../builder/components/edf/EdfOverlayContext';

interface FormFieldShellProps {
  componentId: string;
  style: React.CSSProperties;
  children: React.ReactNode;
}

/**
 * Absolute-positioned field wrapper for public/preview artboard.
 * Lifts z-index while an EDF overlay (dropdown / error / manual panel) is open on this field.
 */
export const FormFieldShell: React.FC<FormFieldShellProps> = ({
  componentId,
  style,
  children,
}) => {
  const lifted = useEdfFieldLifted(componentId);
  const baseZ = typeof style.zIndex === 'number' ? style.zIndex : 1;
  return (
    <div
      style={{
        ...style,
        zIndex: lifted ? Math.max(baseZ, EDF_FIELD_LIFT_Z_INDEX) : baseZ,
      }}
    >
      {children}
    </div>
  );
};
