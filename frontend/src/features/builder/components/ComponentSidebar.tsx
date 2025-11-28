import React from 'react';
import { Box, Type, CheckSquare, AlignLeft, Calendar, Hash, List } from 'lucide-react';

export const ComponentSidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-full overflow-y-auto">
      <div className="p-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-700">Components</h3>
      </div>
      
      <div className="p-4 space-y-6">
        <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Basic Fields</h4>
            <div className="grid grid-cols-2 gap-2">
                <SidebarItem icon={<Type size={18} />} label="Text" />
                <SidebarItem icon={<Hash size={18} />} label="Number" />
                <SidebarItem icon={<AlignLeft size={18} />} label="Textarea" />
                <SidebarItem icon={<Box size={18} />} label="Email" />
            </div>
        </div>

        <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Choice</h4>
            <div className="grid grid-cols-2 gap-2">
                <SidebarItem icon={<CheckSquare size={18} />} label="Checkbox" />
                <SidebarItem icon={<List size={18} />} label="Select" />
                <SidebarItem icon={<Box size={18} />} label="Radio" />
                <SidebarItem icon={<Calendar size={18} />} label="Date" />
            </div>
        </div>
      </div>
    </aside>
  );
};

const SidebarItem: React.FC<{ icon: React.ReactNode; label: string }> = ({ icon, label }) => (
    <div className="flex flex-col items-center justify-center p-3 bg-gray-50 border border-gray-200 rounded hover:bg-teal-50 hover:border-teal-200 hover:text-teal-600 cursor-grab active:cursor-grabbing transition-colors">
        <div className="mb-1 text-gray-500">{icon}</div>
        <span className="text-xs font-medium text-gray-600">{label}</span>
    </div>
);

