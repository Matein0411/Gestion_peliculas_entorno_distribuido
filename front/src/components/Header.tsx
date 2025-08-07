import React from 'react';
import { Film, Database } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 text-white py-6 shadow-2xl">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center space-x-4">
          <div className="flex items-center space-x-3">
            <Film className="h-10 w-10 text-yellow-400" />
            <Database className="h-8 w-8 text-blue-400" />
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-blue-400 bg-clip-text text-transparent">
              CineDB Distribuido
            </h1>
            <p className="text-blue-200 text-lg mt-1">Sistema de Alquiler de Películas - Base de Datos Distribuida</p>
          </div>
          <div className="flex items-center space-x-3">
            <Database className="h-8 w-8 text-blue-400" />
            <Film className="h-10 w-10 text-yellow-400" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;