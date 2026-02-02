import React from 'react';
import type { ComputedFieldStyles } from '../../utils/styleUtils';

export const DividerField: React.FC<{ fieldStyles?: ComputedFieldStyles }> = ({ fieldStyles }) => {
  const color = fieldStyles?.computed.dividerBorderColor || '#E5E7EB';
  const width = fieldStyles?.computed.dividerBorderWidth ?? 1;
  const length = fieldStyles?.computed.dividerWidth || '100%';

  return (
    <div className="py-4 flex items-center justify-center">
      <div
        className="w-full"
        style={{
          width: length,
          maxWidth: '100%',
          borderTopStyle: 'solid',
          borderTopColor: color,
          borderTopWidth: `${width}px`,
        }}
      />
    </div>
  );
};




