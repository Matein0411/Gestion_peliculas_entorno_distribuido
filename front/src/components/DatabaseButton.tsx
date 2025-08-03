import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface DatabaseButtonProps {
  title: string;
  description: string;
  icon: LucideIcon;
  onClick: () => void;
  variant?: 'fragmentation' | 'replication';
}

const DatabaseButton: React.FC<DatabaseButtonProps> = ({ 
  title, 
  description, 
  icon: Icon, 
  onClick, 
  variant = 'fragmentation' 
}) => {
  const baseClasses = "group relative p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl cursor-pointer";
  
  const variantClasses = variant === 'fragmentation' 
    ? "bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200 hover:border-emerald-400 hover:bg-gradient-to-br hover:from-emerald-100 hover:to-teal-100"
    : "bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 hover:border-blue-400 hover:bg-gradient-to-br hover:from-blue-100 hover:to-indigo-100";

  const iconColorClasses = variant === 'fragmentation' 
    ? "text-emerald-600 group-hover:text-emerald-700"
    : "text-blue-600 group-hover:text-blue-700";

  const titleColorClasses = variant === 'fragmentation'
    ? "text-emerald-800 group-hover:text-emerald-900"
    : "text-blue-800 group-hover:text-blue-900";

  return (
    <div className={`${baseClasses} ${variantClasses}`} onClick={onClick}>
      <div className="flex flex-col items-center text-center space-y-3">
        <div className={`p-3 rounded-full ${variant === 'fragmentation' ? 'bg-emerald-100 group-hover:bg-emerald-200' : 'bg-blue-100 group-hover:bg-blue-200'} transition-colors duration-300`}>
          <Icon className={`h-8 w-8 ${iconColorClasses} transition-colors duration-300`} />
        </div>
        <h3 className={`font-bold text-lg ${titleColorClasses} transition-colors duration-300`}>
          {title}
        </h3>
        <p className="text-gray-600 text-sm leading-relaxed">
          {description}
        </p>
      </div>
      
      {/* Efecto de brillo en hover */}
      <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-20 bg-gradient-to-r from-transparent via-white to-transparent transition-opacity duration-300"></div>
    </div>
  );
};

export default DatabaseButton;