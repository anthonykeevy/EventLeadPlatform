/**
 * Form Builder Example - Shows how to integrate with unsaved work tracker
 * 
 * This is a reference implementation showing:
 * 1. How to register with unsaved work tracker
 * 2. How to implement auto-save
 * 3. How to restore drafts
 * 4. How to handle multi-tab scenarios
 * 
 * Delete this file after implementing real form builder
 */

import { useState, useEffect, useCallback } from 'react'
import { useUnsavedWork } from '../utils/unsavedWorkTracker'
import { Save, AlertCircle, CheckCircle } from 'lucide-react'

interface FormBuilderData {
  formId: number | null
  formName: string
  fields: Array<{ id: string; label: string; type: string }>
  settings: Record<string, any>
}

export function FormBuilderExample() {
  const [formData, setFormData] = useState<FormBuilderData>({
    formId: null,
    formName: '',
    fields: [],
    settings: {}
  })
  
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved')
  
  // Register with unsaved work tracker
  const { isDirty, setIsDirty, markClean, markDirty } = useUnsavedWork(
    'form_builder_example',
    'form_builder',
    `Form: ${formData.formName || 'Untitled'}`,
    async () => {
      // Save callback - called when auth changes require save
      await handleSave()
    }
  )
  
  /**
   * Auto-save every 10 seconds
   */
  useEffect(() => {
    if (!isDirty) return
    
    const autoSaveTimer = setTimeout(async () => {
      await handleSave()
    }, 10000) // 10 seconds
    
    return () => clearTimeout(autoSaveTimer)
  }, [formData, isDirty])
  
  /**
   * Restore draft from localStorage on mount
   */
  useEffect(() => {
    const draft = localStorage.getItem('form_builder_draft')
    if (draft) {
      try {
        const parsed = JSON.parse(draft)
        
        const shouldRestore = confirm(
          `Found unsaved changes from ${new Date(parsed.savedAt).toLocaleString()}. Restore?`
        )
        
        if (shouldRestore) {
          setFormData(parsed.data)
          markDirty()
        } else {
          localStorage.removeItem('form_builder_draft')
        }
      } catch (error) {
        console.error('Failed to restore draft:', error)
        localStorage.removeItem('form_builder_draft')
      }
    }
  }, [markDirty])
  
  /**
   * Save form (to backend + localStorage)
   */
  const handleSave = useCallback(async () => {
    setSaveStatus('saving')
    
    try {
      // Save to backend first
      if (formData.formId) {
        // Update existing form
        await fetch(`/api/forms/${formData.formId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('eventlead_access_token')}`
          },
          body: JSON.stringify(formData)
        })
      } else {
        // Create new form
        const response = await fetch('/api/forms', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('eventlead_access_token')}`
          },
          body: JSON.stringify(formData)
        })
        
        const result = await response.json()
        setFormData(prev => ({ ...prev, formId: result.formId }))
      }
      
      // Also save to localStorage (backup)
      localStorage.setItem('form_builder_draft', JSON.stringify({
        data: formData,
        savedAt: new Date().toISOString()
      }))
      
      // Mark as clean
      markClean()
      setLastSaved(new Date())
      setSaveStatus('saved')
      
      console.log('✅ Form saved successfully')
    } catch (error) {
      console.error('Failed to save form:', error)
      
      // Backend failed - at least save to localStorage
      localStorage.setItem('form_builder_draft', JSON.stringify({
        data: formData,
        savedAt: new Date().toISOString(),
        offlineSave: true
      }))
      
      setSaveStatus('unsaved')
      alert('Failed to save to server. Saved locally instead.')
    }
  }, [formData, markClean])
  
  /**
   * Handle form changes
   */
  const handleChange = (field: keyof FormBuilderData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    markDirty()
    setSaveStatus('unsaved')
  }
  
  /**
   * Manual save button
   */
  const handleManualSave = async () => {
    await handleSave()
  }
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Save Status Indicator */}
      <div className="fixed top-4 right-4 bg-white shadow-lg rounded-lg p-3 flex items-center gap-2 border">
        {saveStatus === 'saved' && (
          <>
            <CheckCircle className="w-5 h-5 text-green-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">All changes saved</p>
              {lastSaved && (
                <p className="text-xs text-gray-500">
                  {lastSaved.toLocaleTimeString()}
                </p>
              )}
            </div>
          </>
        )}
        
        {saveStatus === 'saving' && (
          <>
            <div className="w-5 h-5 border-2 border-teal-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm font-medium text-gray-900">Saving...</p>
          </>
        )}
        
        {saveStatus === 'unsaved' && (
          <>
            <AlertCircle className="w-5 h-5 text-yellow-600" />
            <p className="text-sm font-medium text-gray-900">Unsaved changes</p>
          </>
        )}
      </div>
      
      <h1 className="text-2xl font-bold mb-6">Form Builder Example</h1>
      
      {/* Form Builder UI */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Form Name</label>
          <input
            type="text"
            value={formData.formName}
            onChange={(e) => handleChange('formName', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            placeholder="e.g., VIP Registration Form"
          />
        </div>
        
        <div>
          <button
            onClick={handleManualSave}
            disabled={!isDirty || saveStatus === 'saving'}
            className="px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium disabled:opacity-50 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Form
          </button>
        </div>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-900 font-medium mb-2">
            💡 Auto-Save Enabled
          </p>
          <ul className="text-xs text-blue-800 space-y-1">
            <li>• Changes save automatically every 10 seconds</li>
            <li>• Saved to backend AND localStorage (backup)</li>
            <li>• Protected from auth changes in other tabs</li>
            <li>• Browser warns before closing unsaved work</li>
          </ul>
        </div>
      </div>
    </div>
  )
}


