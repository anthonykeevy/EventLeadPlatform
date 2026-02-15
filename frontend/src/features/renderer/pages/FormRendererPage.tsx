import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useBuilderStore } from '../../builder/stores/useBuilderStore';
import { RuntimeFormView } from '../../builder/components/runtime/RuntimeFormView';
import { resolveDefinitionForRender } from '../../builder/utils/definitionResolver';

/**
 * Minimal internal renderer for Story 3.7 runtime parity.
 * Public/optimized renderer is Story 3.8.
 */
export const FormRendererPage: React.FC = () => {
  const { formId } = useParams<{ formId: string }>();
  const { initializeForm, formDefinition, initDefaults, isLoading } = useBuilderStore();

  useEffect(() => {
    if (formId) initializeForm(formId);
  }, [formId, initializeForm]);

  if (isLoading) return <div className="p-6">Loading…</div>;

  if (!formDefinition) {
    return (
      <div className="p-6">
        <p className="text-gray-700">No definition loaded.</p>
        <Link to="/dashboard" className="text-teal-600 hover:underline">Go back</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
        <Link to={`/forms/${formId}/builder`} className="text-gray-600 hover:text-gray-900" aria-label="Back to builder">
          <ArrowLeft size={18} />
        </Link>
        <div className="font-semibold text-gray-900">Renderer (Story 3.7 runtime)</div>
      </header>
      <RuntimeFormView
        definition={resolveDefinitionForRender(initDefaults ?? null, formDefinition)}
        title="Renderer Runtime"
      />
    </div>
  );
};
