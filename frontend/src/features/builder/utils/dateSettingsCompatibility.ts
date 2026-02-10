import { ComponentProps } from '../types/builder.types';

export interface DateSettingIssue {
  key: string;
  reason: string;
  conflictingKeys: string[];
}

export interface DateSettingsCompatibility {
  disabledPickerStyles: Record<string, DateSettingIssue>;
  disabledDateParts: Record<string, DateSettingIssue>;
  warnings: DateSettingIssue[];
  autoFix?: {
    pickerStyle?: ComponentProps['pickerStyle'];
    dateParts?: NonNullable<ComponentProps['dateParts']>;
  };
}

const FULL_DATE_PARTS: NonNullable<ComponentProps['dateParts']> = {
  year: true,
  month: true,
  day: true,
};

const FULL_TIME_PARTS: NonNullable<ComponentProps['dateParts']> = {
  hour: true,
  minute: true,
};

export const getDateSettingsCompatibility = (props: ComponentProps): DateSettingsCompatibility => {
  const dateType = props.dateType ?? 'date';
  const pickerStyle = props.pickerStyle ?? 'calendar';
  const dateParts = props.dateParts ?? FULL_DATE_PARTS;
  const isDateRange = props.validation?.isDateRange ?? false;

  const disabledPickerStyles: Record<string, DateSettingIssue> = {};
  const disabledDateParts: Record<string, DateSettingIssue> = {};
  const warnings: DateSettingIssue[] = [];
  const autoFix: DateSettingsCompatibility['autoFix'] = {};

  if (dateType === 'time') {
    disabledPickerStyles.calendar = {
      key: 'pickerStyle.calendar',
      reason: 'Calendar requires date parts; Time Only uses time controls.',
      conflictingKeys: ['dateType'],
    };
    disabledPickerStyles.dropdown = {
      key: 'pickerStyle.dropdown',
      reason: 'Dropdowns capture Day/Month/Year only (date-only).',
      conflictingKeys: ['dateType'],
    };
  }

  if (dateType === 'datetime') {
    disabledPickerStyles.dropdown = {
      key: 'pickerStyle.dropdown',
      reason: 'Dropdowns capture Day/Month/Year only (no time parts).',
      conflictingKeys: ['dateType'],
    };
  }

  const pickerStyleKey = pickerStyle != null ? pickerStyle : undefined;
  if (pickerStyleKey != null && disabledPickerStyles[pickerStyleKey]) {
    type PickerStyleKey = keyof typeof disabledPickerStyles;
    autoFix.pickerStyle =
      (['calendar', 'native', 'dropdown'] as PickerStyleKey[])
        .find((style) => !disabledPickerStyles[style]) ?? 'native';
    warnings.push({
      key: `pickerStyle.autoFix.${pickerStyle}`,
      reason: `Picker Style "${pickerStyle}" is incompatible with ${dateType}. Auto-selected "${autoFix.pickerStyle}".`,
      conflictingKeys: ['pickerStyle', 'dateType'],
    });
  }

  const usesNativeLikePicker = (pickerStyle === 'native' || pickerStyle === 'calendar');
  const needsFullDateParts = dateType !== 'time' && usesNativeLikePicker;
  const needsFullTimeParts = (dateType === 'time' || dateType === 'datetime') && usesNativeLikePicker;

  if (needsFullDateParts) {
    if (dateParts.year === false || dateParts.month === false || dateParts.day === false) {
      autoFix.dateParts = {
        ...dateParts,
        ...FULL_DATE_PARTS,
      };
      warnings.push({
        key: 'dateParts.autoFix.fullDate',
        reason: 'Calendar/Native pickers always capture full dates. Day/Month/Year were reset to required.',
        conflictingKeys: ['pickerStyle', 'dateParts'],
      });
    }

    disabledDateParts.year = {
      key: 'dateParts.year',
      reason: 'Calendar/Native pickers always include Year.',
      conflictingKeys: ['pickerStyle'],
    };
    disabledDateParts.month = {
      key: 'dateParts.month',
      reason: 'Calendar/Native pickers always include Month.',
      conflictingKeys: ['pickerStyle'],
    };
    disabledDateParts.day = {
      key: 'dateParts.day',
      reason: 'Calendar/Native pickers always include Day.',
      conflictingKeys: ['pickerStyle'],
    };
  }

  if (needsFullTimeParts) {
    if (dateParts.hour === false || dateParts.minute === false) {
      autoFix.dateParts = {
        ...dateParts,
        ...FULL_TIME_PARTS,
      };
      warnings.push({
        key: 'dateParts.autoFix.fullTime',
        reason: 'Calendar/Native pickers require Hour and Minute. Time parts were reset to required.',
        conflictingKeys: ['pickerStyle', 'dateParts'],
      });
    }

    disabledDateParts.hour = {
      key: 'dateParts.hour',
      reason: 'Calendar/Native pickers always include Hour.',
      conflictingKeys: ['pickerStyle'],
    };
    disabledDateParts.minute = {
      key: 'dateParts.minute',
      reason: 'Calendar/Native pickers always include Minute.',
      conflictingKeys: ['pickerStyle'],
    };
  }

  if (pickerStyle === 'native' && dateType !== 'time') {
    warnings.push({
      key: 'dateFormat.nativeWarning',
      reason: 'Native pickers control the visual format. Display Format applies only to stored/displayed values.',
      conflictingKeys: ['pickerStyle', 'dateFormat'],
    });
  }

  const hasPartialDateParts =
    dateType !== 'time' && (dateParts.year === false || dateParts.month === false || dateParts.day === false);
  if (pickerStyle !== 'dropdown' && hasPartialDateParts) {
    warnings.push({
      key: 'dateParts.partialWarning',
      reason: 'Partial date parts are only supported by Dropdowns (Day/Month/Year).',
      conflictingKeys: ['pickerStyle', 'dateParts'],
    });
  }

  if (isDateRange) {
    warnings.push({
      key: 'dateRange.pickerWarning',
      reason: 'Date Range validation is enabled, but current pickers only capture a single date.',
      conflictingKeys: ['validation.isDateRange', 'pickerStyle'],
    });
  }

  return {
    disabledPickerStyles,
    disabledDateParts,
    warnings,
    autoFix: Object.keys(autoFix).length > 0 ? autoFix : undefined,
  };
};
