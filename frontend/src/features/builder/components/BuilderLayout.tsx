import React from 'react';
import { ArrowLeft, Settings, Save, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';

interface BuilderLayoutProps {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  title?: string;
}

export const BuilderLayout: React.FC<BuilderLayoutProps> = ({ children, sidebar, title }) => {
  return (
    <div className="flex flex-col h-screen bg-gray-100 overflow-hidden">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between flex-shrink-0 z-10 shadow-sm">
        <div className="flex items-center gap-4">
            <Link to="/dashboard" className="text-gray-500 hover:text-gray-800 transition-colors">
                <ArrowLeft size={20} />
            </Link>
            <div className="h-6 w-px bg-gray-200"></div>
            <h1 className="font-semibold text-gray-800 text-lg">{title || 'Untitled Form'}</h1>
            <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded-full font-medium">Draft</span>
        </div>

        <div className="flex items-center gap-3">
            <button className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2">
                <Eye size={16} /> Preview
            </button>
            <button className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2">
                <Settings size={16} /> Settings
            </button>
            <button className="btn-primary text-sm py-1.5 px-4 flex items-center gap-2">
                <Save size={16} /> Save
            </button>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar (Toolbox) */}
        {sidebar}

        {/* Center Canvas */}
        <main className="flex-1 overflow-y-auto bg-gray-100 relative">
             {children}
        </main>

        {/* Right Sidebar (Properties - Placeholder) */}
        <aside className="w-80 bg-white border-l border-gray-200 flex-shrink-0 hidden lg:block">
            <div className="p-4 border-b border-gray-100">
                <h3 className="font-semibold text-gray-700">Properties</h3>
            </div>
            <div className="p-8 text-center text-gray-400 text-sm">
                Select a component to edit its properties.
                <br/>(Coming in Story 3.5)
            </div>
        </aside>
      </div>
    </div>
  );
};

