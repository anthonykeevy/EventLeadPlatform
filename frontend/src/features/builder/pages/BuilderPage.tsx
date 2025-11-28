import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useBuilderStore } from '../stores/useBuilderStore';
import { BuilderLayout } from '../components/BuilderLayout';
import { ComponentSidebar } from '../components/ComponentSidebar';
import { FormBuilderCanvas } from '../components/FormBuilderCanvas';
import { LoadingSpinner } from '../../ux/components/LoadingSpinner';

export const BuilderPage: React.FC = () => {
  const { formId } = useParams<{ formId: string }>();
  const { initializeForm, isLoading, formDefinition } = useBuilderStore();

  useEffect(() => {
    if (formId) {
      initializeForm(formId);
    }
  }, [formId, initializeForm]);

  if (isLoading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
            <LoadingSpinner size="large" />
            <p className="mt-4 text-gray-500">Loading Form Builder...</p>
        </div>
      </div>
    );
  }

  return (
    <BuilderLayout 
        sidebar={<ComponentSidebar />}
        title={formDefinition?.formId ? `Form: ${formDefinition.formId}` : 'Form Builder'}
    >
      <FormBuilderCanvas />
    </BuilderLayout>
  );
};

